# IE400 Fall 2023 Term Project - Part 1
# Group 41
# Cagatay Safak - 21902730
# Ayse Kelleci - 21902532

import cplex

# Function to calculate the distance of a path
def calculate_path_distances(paths, distance_data):
    distances = []

    # Create a dictionary to map node names to indices
    node_indices = {chr(65 + i): i for i in range(len(distance_data))}

    for path in paths:
        total_distance = 0.0

        # Calculate distance for each edge in the path
        for i in range(len(path) - 1):
            start_node = path[i]
            end_node = path[i + 1]

            # Get the indices corresponding to the start and end nodes
            start_index = node_indices[start_node]
            end_index = node_indices[end_node]

            # Accumulate the distance based on the distance data
            total_distance += distance_data[start_index][end_index]

        distances.append(total_distance)

    return distances

noOfTrains = 15
noOfStation = 10 # including depots
noOfDepots = 2
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

paths = []
distances = []
depot_node_distances = []
depotX_distances = []
depotY_distances = []
startToX = []
startToY = []
endToX = []
endToY = []

# READING PATHS.TXT
with open('paths.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split the line by ':' to separate index and path
        index, path = line.strip().split(': ')
        # Split the path by '-' to create a list of nodes
        path_list = path.split('-')
        # Append the path list to the paths list
        paths.append(path_list)

# READING DISTANCES.TXT
with open('distances.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split the line by spaces and convert each value to float
        row = [float(val) for val in line.strip().split()]
        # Append the row to the values list
        distances.append(row)
        
# READING DEPOT_NODE_DISTANCES.TXT
with open('depot_node_distances.txt', 'r') as file:
    for line in file:
        # Split the line by ': ' to separate identifier and path
        _, path = line.strip().split(': ')
        # Split the path by '-' to create a list of nodes and append to combined_paths
        depot_node_distances.append(path.split('-'))
        
depotX_distances = depot_node_distances[0]
depotY_distances = depot_node_distances[1]

# CALCULATING THE DISTANCE OF EACH PATH
path_distances = calculate_path_distances(paths, distances)

# CALCULATING THE DISTANCE FROM START AND END NODES OF PATHS TO DEPOTS
node_indices = {chr(65 + i): i for i in range(len(depotX_distances))}
for path in paths:
    start_node = path[0]
    end_node = path[-1]

    startToX.append(int(depotX_distances[node_indices[start_node]]))
    startToY.append(int(depotY_distances[node_indices[start_node]]))
    endToX.append(int(depotX_distances[node_indices[end_node]]))
    endToY.append(int(depotY_distances[node_indices[end_node]]))

# CREATING pathsStartingWith LIST
pathsStartingWith = [[int(path[0] == node) for node in nodes] for path in paths]

# PRINTING THE PARAMETERS, UNCOMMENT TO SEE
#
# for idx, path in enumerate(paths, 1):
#     print(f"Path {idx}: {path}")
# for row in distances:
#     print(row)
# print(f"Combined Paths: {depot_node_distances}")
# for i, distance in enumerate(path_distances, start=1):
#     print(f"Distance for Path {i}: {distance}")
# print(depotX_distances)
# print(depotY_distances)
# print("startToX:", startToX)
# print("startToY:", startToY)
# print("endToX:", endToX)
# print("endToY:", endToY)
# for i, path in enumerate(pathsStartingWith, start=1):
#     print(f"Path {i}: {path}")

# Create a modeling problem instance
model = cplex.Cplex()

x = []
for i in range(noOfTrains):
    x.append(model.variables.add(obj=[startToX[i] + endToX[i], startToY[i] + endToY[i]], types=['B', 'B']))
    
# Set objective function: Minimize the sum of (startToX_i + endToX_i) * x_i1 + (startToY_i + endToY_i) * x_i2
model.objective.set_sense(model.objective.sense.minimize)

# Define constraints
# Sum of x_i1's from i=1 to i=15 must be >= 5
model.linear_constraints.add(
    lin_expr=[[list(range(noOfTrains)), [1] * noOfTrains]],
    senses='G',
    rhs=[5]
)

# Sum of x_i2's from i=1 to i=15 must be >= 5
model.linear_constraints.add(
    lin_expr=[[list(range(noOfTrains)), [1] * noOfTrains]],
    senses='G',
    rhs=[5]
)

# x_i1 + x_i2 = 1, for all i's
for i in range(noOfTrains):
    constraint_indices = [x[i][0], x[i][1]]  # Decision variable indices for train i
    constraint_values = [1.0, 1.0]  # Coefficients for x_i1 and x_i2

    # Add the constraint x_i1 + x_i2 = 1 for each train i
    model.linear_constraints.add(
        lin_expr=[[constraint_indices, constraint_values]],
        senses='E',
        rhs=[1],
        names=[f'constraint_{i}']
    )

# Additional constraint: sum of k's in 1-8 (sum of i's in 1-15 (x_ij * pathsStartingWith)) <= 3
for k in range(8):  # Nodes from 1 to 8
    for j in range(2):  # Depots
        constraint_expr = [
            [i, x[i][j]] for i in range(noOfTrains)
            if pathsStartingWith[i][k] == 1
        ]
        constraint_indices = [constraint_expr[i][1] for i in range(len(constraint_expr))]
        constraint_values = [1.0] * len(constraint_expr)

        model.linear_constraints.add(
            lin_expr=[[constraint_indices, constraint_values]],
            senses='L',
            rhs=[3],
            names=[f'node_constraint_{k}_{j}']
        )

# Solve the problem
model.solve()

# Retrieve solution and print results
solution = model.solution

# for i in range(noOfTrains):
#     print(f"Train {i+1} assigned to Depot 1: {solution.get_values(f'x[{i}][0]')}, Depot 2: {solution.get_values(f'x[{i}][1]')}")

print("Obj Value:", model.solution.get_objective_value())
print("Values of Decision Variables:", model.solution.get_values())

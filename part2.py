# IE400 Fall 2023 Term Project - Part 2
# Group 41
# Cagatay Safak - 21902730
# Ayse Kelleci - 21902532

import cplex
from docplex.mp.model import Model

# part1res = model.solution.get_values()
# train_depots = [] # X or Y

# for i in range(noOfTrains):
#     if part1res[2*i] == 1:
#         train_depots.append("X")
#     else:
#         train_depots.append("Y")

# print("Train Depots:", train_depots)


# IMPORTANT NOTE FOR THE FOLLOWING PARTS:
#
# MOST OF THE DATA HARDCODED BELOW ARE OBTAINED FROM PART 1. ALL OF THEM HAS AN EXACT 
# CORRESPONDING VARIABLE IN PART 1.
node_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
startToX = [1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
startToY = [3, 2, 1, 1, 1, 2, 3, 2, 1, 1, 3, 3, 2, 1, 2]
endToX = [1, 1, 2, 1, 1, 2, 3, 1, 1, 3, 1, 2, 2, 3, 1]
endToY = [2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1]
train_depots = ['X', 'X', 'Y', 'Y', 'Y', 'X', 'Y', 'X', 'X', 'Y', 'X', 'X', 'Y', 'Y', 'X']
noOfTrains = len(train_depots)
train_to_depot = []
path_distances = [7.0, 3.0, 4.0, 9.0, 3.0, 2.0, 5.0, 5.0, 4.0, 9.0, 2.0, 2.0, 5.0, 5.0, 2.0]
noOfCycles = []
node_distances = [[0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0],
                  [1.0, 0.0, 1.0, 1.0, 2.0, 3.0, 1.0, 3.0],
                  [2.0, 1.0, 0.0, 1.0, 2.0, 2.0, 3.0, 2.0],
                  [1.0, 1.0, 1.0, 0.0, 1.0, 2.0, 1.0, 2.0],
                  [1.0, 2.0, 2.0, 1.0, 0.0, 1.0, 3.0, 2.0],
                  [2.0, 3.0, 2.0, 2.0, 1.0, 0.0, 1.0, 2.0],
                  [2.0, 1.0, 3.0, 1.0, 3.0, 1.0, 0.0, 1.0],
                  [1.0, 3.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0]]
paths = [['A', 'C', 'H', 'B'],
         ['B', 'G', 'A'],
         ['C', 'G', 'D'],
         ['D', 'F', 'E', 'G', 'C'],
         ['E', 'F', 'C'],
         ['H', 'G', 'F'],
         ['A', 'H', 'G', 'E'],
         ['B', 'H', 'C'],
         ['C', 'E', 'H'],
         ['F', 'G', 'E', 'A', 'B', 'C', 'D', 'E'],
         ['A', 'B', 'C'],
         ['A', 'F'],
         ['B', 'F', 'D'],
         ['G', 'C', 'E'],
         ['B', 'D', 'G']]

for i in range(noOfTrains):
    if train_depots[i] == 'X':
        train_to_depot.append(startToX[i] + endToX[i])
    else:
        train_to_depot.append(startToY[i] + endToY[i])
endToDepot = []
for i in range(noOfTrains):
    if train_depots[i] == 'X':
        endToDepot.append(endToX[i])
    else:
        endToDepot.append(endToY[i])
startToDepot = []
for i in range(noOfTrains):
    if train_depots[i] == 'X':
        startToDepot.append(startToX[i])
    else:
        startToDepot.append(startToY[i])

first_elements = [path[0] for path in paths]  # Extract the first elements of each sublist
last_elements = [path[-1] for path in paths]  # Extract the last elements of each sublist

# get duration of each path by using path_distances. max duration is 20 hours per day
# ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION ACTUAL ITERATION 
path_durations = []
noOfCycles = []
exact_paths = [[] for _ in range(15)]
exact_timestamps = [[] for _ in range(15)]
for i in range(noOfTrains):
    duration = path_distances[i]
    path_durations.append(duration + startToDepot[i])
    noOfCycles.append(1)
    return_distance = node_distances[node_names.index(first_elements[i])][node_names.index(last_elements[i])]
    exact_paths[i].append(train_depots[i])
    for j in range(len(paths[i])):
        exact_paths[i].append(paths[i][j])
    while path_durations[i] + duration + return_distance <= (20 - endToDepot[i]):
        path_durations[i] += duration + return_distance
        noOfCycles[i] += 1
        for j in range(len(paths[i])):
            exact_paths[i].append(paths[i][j])
    path_durations[i] += endToDepot[i]
    exact_paths[i].append(train_depots[i])

for i in range(len(exact_paths)):
    exact_timestamps[i].append(0)
    exact_timestamps[i].append(startToDepot[i])
    # for loop starting from 2 ending at len(exact_paths[i]) - 1
    for j in range(2, len(exact_paths[i]) - 1):
        exact_timestamps[i].append(exact_timestamps[i][j-1] + node_distances[node_names.index(exact_paths[i][j-1])][node_names.index(exact_paths[i][j])])
    exact_timestamps[i].append(exact_timestamps[i][-1] + endToDepot[i])

print("noOfCycles:", noOfCycles)
print("path_durations:", path_durations)
print("exact_paths:", exact_paths)
print("exact_timestamps:", exact_timestamps)
print("train_depots:", train_depots)

# Define costs
cost_purchase_electric = 750000
cost_purchase_diesel = 250000
cost_energy_diesel = 100000
cost_energy_electric = 20000

unique_nodes = set([node for path in exact_paths for node in path])

# Create a model
mdl = Model('TrainOptimization')

# Decision variables
num_trains = len(train_depots)
unique_nodes = set([node for path in exact_paths for node in path])
depots = {'X', 'Y'}  # Assuming X and Y are the depots
node_to_index = {node: idx for idx, node in enumerate(unique_nodes)}
num_nodes = len(unique_nodes)
E = mdl.binary_var_list(num_trains, name='E')  # Electric train decision
s = mdl.integer_var_list(num_nodes, name='s')  # Charging stations at each node

# Objective function components
depot_station_cost = mdl.sum(s[node_to_index[node]] * 1000000 for node in depots if node in unique_nodes)
on_route_station_cost = mdl.sum(s[node_to_index[node]] * 350000 for node in unique_nodes if node not in depots)
purchase_cost = mdl.sum(E[i] * 750000 + (1 - E[i]) * 250000 for i in range(num_trains))
energy_cost = mdl.sum(path_durations[i] * (E[i] * 20000 + (1 - E[i]) * 100000) for i in range(num_trains))

# Total cost
mdl.minimize(depot_station_cost + on_route_station_cost + purchase_cost + energy_cost)

# Constraints
# Electric train charging constraint
for i in range(num_trains):
    time_since_last_charge = 0
    for k in range(1, len(exact_paths[i])):
        time_since_last_charge += exact_timestamps[i][k] - exact_timestamps[i][k - 1]
        if time_since_last_charge >= 8:
            # A charging station is needed at this node
            node = exact_paths[i][k]
            mdl.add_constraint(s[node_to_index[node]] >= 1)
            time_since_last_charge = 0  # Reset the counter after charging

# Solve the model
solution = mdl.solve()

# Output the solution and final cost
if solution:
    for i in range(num_trains):
        print(f"Train {i} is {'electric' if E[i].solution_value == 1 else 'diesel'}")
    for node in unique_nodes:
        if s[node_to_index[node]].solution_value > 0:
            print(f"Node {node} has {s[node_to_index[node]].solution_value} charging stations")
    print(f"Final Total Cost: {solution.get_objective_value()}")
else:
    print("No solution found")
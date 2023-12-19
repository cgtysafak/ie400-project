# IE400 Fall 2023 Term Project - Part 2
# Group 41
# Cagatay Safak - 21902730
# Ayse Kelleci - 21902532

import cplex

# part1res = model.solution.get_values()
# train_depots = [] # X or Y

# for i in range(noOfTrains):
#     if part1res[2*i] == 1:
#         train_depots.append("X")
#     else:
#         train_depots.append("Y")

# print("Train Depots:", train_depots)

# # get duration of each path by using path_distances. max duration is 20 hours per day
# path_durations = []
# for i in range(noOfTrains):
#     duration = path_distances[i]
#     path_durations.append(duration)
#     while path_durations[i] + duration <= 20:
#         path_durations[i] += duration

# Define train depots and path durations
train_depots = ['X', 'X', 'Y', 'Y', 'Y', 'X', 'Y', 'X', 'X', 'Y', 'X', 'X', 'Y', 'Y', 'X']
path_durations = [14.0, 18.0, 20.0, 18.0, 18.0, 20.0, 20.0, 20.0, 20.0, 18.0, 20.0, 20.0, 20.0, 20.0, 20.0]
noOfTrains = len(train_depots)

# Define costs
cost_purchase_electric = 750000
cost_purchase_diesel = 250000
cost_energy_diesel = 100000
cost_energy_electric = 20000

# Create a modeling problem instance
model2 = cplex.Cplex()

# Define decision variables: y_ij = 0 if train i is electric, 1 if it's diesel
y = []
for i in range(noOfTrains):
    y.append(model2.variables.add(obj=[cost_energy_electric * path_durations[i] + cost_purchase_electric, cost_energy_diesel * path_durations[i] + cost_purchase_diesel], types=['B', 'B']))

# Set objective function: Minimize total operational cost
model2.objective.set_sense(model2.objective.sense.minimize)

# Define constraints
# x_i1 + x_i2 = 1, for all i's
for i in range(noOfTrains):
    constraint_indices = [y[i][0], y[i][1]]  # Decision variable indices for train i
    constraint_values = [1.0, 1.0]  # Coefficients for x_i1 and x_i2

    # Add the constraint x_i1 + x_i2 = 1 for each train i
    model2.linear_constraints.add(
        lin_expr=[[constraint_indices, constraint_values]],
        senses='E',
        rhs=[1],
        names=[f'constraint_{i}']
    )

# Purchase cost constraint
for i in range(noOfTrains):
    model2.linear_constraints.add(
        lin_expr=[[list(range(2 * i, 2 * i + 2)), [1.0, 1.0]]],
        senses='G',
        rhs=[0],
        names=[f'purchase_cost_constraint_{i}']
    )

# Solve the problem
model2.solve()

print("Values of Decision Variables:", model2.solution.get_values())
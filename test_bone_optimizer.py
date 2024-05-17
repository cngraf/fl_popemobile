# import pulp

# # Define the problem
# prob = pulp.LpProblem("Skeleton_Assembly", pulp.LpMaximize)

# # Parameters (example values)
# c_T2, c_T4 = 30, 50
# c_L1, c_L2 = 20, 25
# m1, m2 = 0.2, 0.3
# t_L2, t_L4 = 2, 4
# a_T2, a_T4 = 10, 15
# a_L1, a_L2 = 5, 8
# M_T2, M_T4 = 5, 7
# M_L1, M_L2 = 3, 4
# budget = 1000
# T = 500

# # Decision variables
# y2 = pulp.LpVariable("y2", lowBound=0, cat='Integer')
# y4 = pulp.LpVariable("y4", lowBound=0, cat='Integer')
# xT2 = pulp.LpVariable("xT2", lowBound=0, cat='Integer')
# xT4 = pulp.LpVariable("xT4", lowBound=0, cat='Integer')
# xL1 = pulp.LpVariable("xL1", lowBound=0, cat='Integer')
# xL2 = pulp.LpVariable("xL2", lowBound=0, cat='Integer')

# # Binary variables for torso inclusion
# z2_2 = pulp.LpVariable("z2_2", cat='Binary')  # y2 uses T2
# z2_4 = pulp.LpVariable("z2_4", cat='Binary')  # y2 uses T4
# z4_2 = pulp.LpVariable("z4_2", cat='Binary')  # y4 uses T2
# z4_4 = pulp.LpVariable("z4_4", cat='Binary')  # y4 uses T4

# # Binary variables for limb inclusion
# w2_1 = pulp.LpVariable("w2_1", cat='Binary')  # y2 uses L1
# w2_2 = pulp.LpVariable("w2_2", cat='Binary')  # y2 uses L2
# w4_1 = pulp.LpVariable("w4_1", cat='Binary')  # y4 uses L1
# w4_2 = pulp.LpVariable("w4_2", cat='Binary')  # y4 uses L2

# # Objective function
# profit = (
#     (1 + m1) * (c_T2 + t_L2 * (c_L1 + c_L2)) * y2 +
#     (1 + m2) * (c_T4 + t_L4 * (c_L1 + c_L2)) * y4 +
#     (a_T2 * z2_2 + a_T4 * z2_4 + a_L1 * w2_1 + a_L2 * w2_2) * (M_T2 * z2_2 + M_T4 * z2_4 + M_L1 * w2_1 + M_L2 * w2_2) +
#     (a_T2 * z4_2 + a_T4 * z4_4 + a_L1 * w4_1 + a_L2 * w4_2) * (M_T2 * z4_2 + M_T4 * z4_4 + M_L1 * w4_1 + M_L2 * w4_2)
# )
# cost = (
#     c_T2 * xT2 + c_T4 * xT4 + c_L1 * xL1 + c_L2 * xL2
# )
# prob += profit - cost

# # Constraints
# prob += xL1 + xL2 == t_L2 * xT2 + t_L4 * xT4, "Limb-to-Torso Match"
# prob += cost <= budget, "Budget Constraint"
# prob += xT2 + xT4 + xL1 + xL2 + 2 * xT2 + 4 * xT4 + 3 * (y2 + y4) <= T, "Time Constraint"
# prob += y2 <= z2_2 * xT2 + z2_4 * xT4, "Linking Skeletons to Torsos for y2"
# prob += y4 <= z4_2 * xT2 + z4_4 * xT4, "Linking Skeletons to Torsos for y4"
# prob += y2 <= w2_1 * xL1 + w2_2 * xL2, "Linking Skeletons to Limbs for y2"
# prob += y4 <= w4_1 * xL1 + w4_2 * xL2, "Linking Skeletons to Limbs for y4"

# # Solve the problem
# prob.solve()

# # Print the results
# print(f'Optimal number of two-limbed skeletons: {pulp.value(y2)}')
# print(f'Optimal number of four-limbed skeletons: {pulp.value(y4)}')
# print(f'Optimal number of two-limbed torsos: {pulp.value(xT2)}')
# print(f'Optimal number of four-limbed torsos: {pulp.value(xT4)}')
# print(f'Optimal number of limbs (type 1): {pulp.value(xL1)}')
# print(f'Optimal number of limbs (type 2): {pulp.value(xL2)}')

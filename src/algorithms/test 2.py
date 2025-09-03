import common
import sa

n = int(input())
dist = []
for i in range(n):
    row = [int(x) for x in input().split()]
    dist.append(row)
tsp_input = common.TSP_input(n, dist, None)
parameters = common.SA_parameters(0.98, 3000, 5000)
best_iteration, aco_output = sa.solve_sa(tsp_input, parameters)
print(best_iteration)
print(aco_output[best_iteration].path)
print(aco_output[best_iteration].cost)


"""
parameters = common.ACO_parameters(2, 3, 50, 0.6, 40, 20, 1)
best_iteration, aco_output = aco.solve_aco(tsp_input, parameters)
print(best_iteration)
print(aco_output[best_iteration].best_route)
print(aco_output[best_iteration].cost)
"""
#hk = held_karp.held_karp(tsp_input)
#print(hk.cost)
#print(hk.path)
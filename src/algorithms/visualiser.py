from common import *
#from aco import *
import matplotlib.pyplot as plt
import math
import random
#from sa import *
from held_karp import *

def generate_random_tsp(n):
    coordinates = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    
    dist = [[-1 if i == j else math.dist(coordinates[i], coordinates[j]) 
             for j in range(n)] for i in range(n)]
    
    return TSP_input(n, dist, coordinates)


def visualize_routes(route1, route2, route3, points):
    plt.figure()
    
    for i in range(-1, len(route1) - 1):
        plt.plot([points[route1[i]][0], points[route1[i+1]][0]],
                 [points[route1[i]][1], points[route1[i+1]][1]], 'pink')
    
    for i in range(-1, len(route2) - 1):
        plt.plot([points[route2[i]][0], points[route2[i+1]][0]],
                 [points[route2[i]][1], points[route2[i+1]][1]], 'orange')
    
    for i in range(-1, len(route3) - 1):
        plt.plot([points[route3[i]][0], points[route3[i+1]][0]],
                 [points[route3[i]][1], points[route3[i+1]][1]], 'blue')
    
    plt.scatter(*zip(*points), s=100, c='purple', marker='o')
    plt.show()
    
    

def main():
    
    n_cities = 16
    tsp_input = generate_random_tsp(n_cities)

    parameters = ACO_parameters(2, 3, 100, 0.6, 25, 50, 0)
    sa_parameters = SA_parameters(0.97, 1000, 1000)
    
    
    best, found, route = solve_aco(tsp_input, parameters)
    sa_best, sa_found, sa_route = solve_sa(tsp_input, sa_parameters)
    print(1)
    hk_best, hk_path = held_karp(tsp_input)
    print(hk_path)
    
    print("ACO best: ", str(best), " found: ", str(found))
    print("SA best: ", str(sa_best), " found: ", str(sa_found))
    print("Actual best (held-karp): ", str(hk_best))
    visualize_routes(route, sa_route, hk_path, tsp_input.coordinates)

def test_hk():
    n_cities = 15
    tsp_input = generate_random_tsp(n_cities)

    hk_output = held_karp(tsp_input)
    print(hk_output.path)
    print("Actual best (held-karp): ", str(hk_output.cost))


"""
def test_sa():
    n_cities = 10
    tsp_input = generate_random_tsp(n_cities)
    sa_parameters = SA_parameters(0.95, 100, 100)
    
    solve_sa_with_display(tsp_input, sa_parameters)


test_sa()
"""
test_hk()
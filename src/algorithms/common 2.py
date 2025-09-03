import math

inf = 10000000000
max_n = 15 #for held karp
        
class TSP_input():
    def __init__(self, n, dist, coordinates):
        self.n = n
        self.dist = dist
        self.coordinates = coordinates


class ACO_parameters():
    def __init__(self, alpha, beta, Q, evaporation_rate, n_ants, iterations, shake):
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.evaporation_rate = evaporation_rate
        self.n_ants = n_ants
        self.iterations = iterations
        self.shake = shake
        
class ACO_output():
    def __init__(self, n, n_ants, ant_route, best_route, pheromone, cost):
        self.n = n
        self.n_ants = n_ants
        self.ant_route = ant_route
        self.best_route = best_route
        self.pheromone = pheromone
        self.cost = cost
        
        
class SA_parameters():
    def __init__(self, alpha, T, iterations):
        self.alpha = alpha
        self.T = T
        self.iterations = iterations
        
class SA_output():
    def __init__(self, T, path, cost, probability):
        self.T = T
        self.path = path
        self.cost = cost
        self.probability = probability

class heldkarp_output():
    def __init__(self, cost, path):
        self.path = path
        self.cost = cost


def calculate_distance_matrix(coordinates):
    dist = []
    n = len(coordinates)

    for [x1, y1] in coordinates:
        dist_row = []
        for [x2, y2] in coordinates:
            dist_row.append(math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2)))
        dist.append(dist_row)
    return n, dist

        
        
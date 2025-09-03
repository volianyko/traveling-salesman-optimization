from math import exp
from algorithms.common import *
import numpy as np
import random
import copy
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
"""


class Graph():
    def __init__(self, n, dist, coordinates): #n - number of cities, dist - distance matrix

        if n==0: # check if any cities are given
            return "No cities are given"
        if n!=len(dist) or n!=len(dist[0]): #check if the size of matrix is correct
            return "The size of the distance matrix isn't correct"


        self.n = n
        for i in range(n):
            for j in range(n):   
                if i == j:   dist[i][j] = inf

        self.dist = dist
        self.coordinates = coordinates
    

class State():
    def __init__(self, graph, **kwargs):
        type = kwargs['type']

        if type == "random": #if a random state has to be generated, use the generate_random_state() function
            self.generate_random_state(graph)

        elif type == "neighbour": #if a neighbouring state has to be generated, retrieve the current state attrbute and modify it to create a different state
            current_state = kwargs["current_state"]
            self.path = current_state.path
            self.generate_neighbour_state(graph)
        
        else:
            return
        
        self.calculate_cost(graph) # finaly, calculate the cost of the state
    

    def calculate_cost(self, graph):
        self.cost = 0 #initialise cost as 0
        for i in range(1, len(self.path)):
            self.cost += graph.dist[self.path[i]][self.path[i-1]] #add the weight of each edge in the path
        
    
    def generate_random_state(self, graph):
        n = graph.n
        array = np.array(list(range(n))) #generate an array [0, 1, 2, ..., n]
        path = np.random.permutation(array) #shuffle the array to create a random path
        path = np.concatenate((path, [path[0]])) #append the first node to the end to create a cycle

        self.path = path
    
    def generate_neighbour_state(self, graph):

        self.path = self.path[:-1] #cut the last node as it's a repeat of the first node 

        x = random.randint(1, 4) #generate a random number to choose one of 3 modifications
        if x==1:
            self.swap_two_nodes()
        elif x==2:
            self.reverse_segment()
        elif x==3:
            self.insert_random_node()
        else:
            self.insert_random_segment()
        
        self.path = np.concatenate((self.path, [self.path[0]])) #append the fist node to the end to create a cycle
    

    
    def swap_two_nodes(self):
        index = random.randint(0, len(self.path)-2) #choose a random index
        self.path[index], self.path[index+1] = self.path[index+1], self.path[index] #swap 2 neighbouring nodes
    
    def reverse_segment(self):
        #choose 2 distinct random numbers from 0 to n-1 (we're using sample function so that they are distinct)
        index1, index2 = random.sample(range(len(self.path)), 2) 
        start, end = min(index1, index2), max(index1, index2) #assign start and end of the segment

        self.path[start:end+1] = self.path[start:end+1][::-1] #reverse the segment

    def insert_random_node(self):
        
        index_to_move = random.randint(0, len(self.path)-1) # choose a random index for the item to be moved
        # choose a random destination index different from the source index
        index_destination = random.choice([i for i in range(len(self.path)) if i != index_to_move])

        # move the item to the new position
        item_to_move = self.path[index_to_move]
        self.path = np.delete(self.path, index_to_move)
        self.path = np.insert(self.path, index_destination, item_to_move)
    
    
    def insert_random_segment(self):
        #choose 2 random indecies
        index1, index2 = random.sample(range(self.path.size), 2)
        start, end = min(index1, index2), max(index1, index2)
       
        segment = self.path[start:end+1] # extract the random segment
        self.path = np.delete(self.path, slice(start, end+1)) # delete the segment from the original position
        
        index_destination = random.randint(0, self.path.size)# choose a random destination index different from the source index
        self.path = np.insert(self.path, index_destination, segment)# insert the segment at the new position
        

class SA():
    #function to initialise the problem
    def __init__(self, graph_params, sa_params): 
        self.graph = Graph(graph_params.n, graph_params.dist, graph_params.coordinates) #create a graph object
        #store sa parameters in SA object
        self.T = sa_params.T 
        self.alpha = sa_params.alpha
        self.state = State(self.graph, type="random") #create a random state
    
    def iteration(self):
        
        #generate a neighbouring state
        current_state = self.state
        new_state = State(self.graph, type="neighbour", current_state = copy.deepcopy(current_state))
        
        accept = False
        probability = 1
        
        #if cost of new state is less, accept it
        if new_state.cost < current_state.cost:
            accept = True
        
        #if not, accept it with probability P = exp(-dC/T)
        else:
            delta_cost = new_state.cost - current_state.cost
            probability = exp(-delta_cost/self.T)
            
            if probability >= random.random():
                accept = True
        
        if accept:
            self.state = copy.deepcopy(new_state)
        
        # Temperature decay 
        self.T = self.alpha*self.T
        
        output = SA_output(self.T, current_state.path.tolist(), current_state.cost, probability) 
        
        return output


def solve_sa(tsp_input, sa_params):
    sa = SA(tsp_input, sa_params) #initialise the problem
    output = []
    best = inf
    best_found = 0

    for iteration in range(sa_params.iterations):
        
        iteration_output = sa.iteration()
        output.append(iteration_output)

        if iteration_output.cost < best: #if the length is less than the best length stored#
            #update the best solution
            best = iteration_output.cost
            best_found = iteration
    
    return best_found, output


"""
def solve_sa_with_display(tsp_input, sa_params):
    sa = SA(tsp_input, sa_params)

    # Lists to store values for plotting
    paths, costs, temperatures, probabilities = [], [], [], []

    # Setting up the plot in a 2x2 layout
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    

    def update(frame):
        # Perform an iteration
        sa_output = sa.iteration()

        # Update lists for plotting
        paths.append(sa_output.path)
        costs.append(sa_output.cost)
        temperatures.append(sa_output.T)
        probabilities.append(sa_output.probability)

        # Clear previous plots
        for ax in axs.flat:
            ax.clear()

        # Plotting the path
        path = paths[-1]
        x = [tsp_input.coordinates[i][0] for i in path]
        y = [tsp_input.coordinates[i][1] for i in path]
        axs[0, 0].plot(x, y, marker='o')
        axs[0, 0].set_title("Path")

        # Plotting cost graph
        axs[0, 1].plot(costs, color='blue')
        axs[0, 1].set_title("Cost over Iterations")

        # Plotting temperature graph
        axs[1, 0].plot(temperatures, color='red')
        axs[1, 0].set_title("Temperature over Iterations")

        # Plotting probability graph as dots
        axs[1, 1].scatter(range(len(probabilities)), probabilities, color='green')
        axs[1, 1].set_title("Acceptance Probability")

        # Draw the plots
        plt.draw()

    # Create animation
    ani = FuncAnimation(fig, update, frames=sa_params.iterations, repeat=False)

    plt.show()
    return paths[-1], costs[-1], temperatures[-1]


def solve_sa_with_display_non_animated(tsp_input, sa_params):
    sa = SA(tsp_input, sa_params)

    # Lists to store values for plotting
    paths, costs, temperatures, probabilities = [], [], [], []

    # Setting up the plot in a 2x2 layout
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    best = inf
    found = 0
    best_route = None

    for i in range(sa_params.iterations):
        # Perform an iteration
        sa_output = sa.iteration()

        # Update lists for plotting
        paths.append(sa_output.path)
        costs.append(sa_output.cost)
        temperatures.append(sa_output.T)
        probabilities.append(sa_output.probability)

        if sa_output.cost < best: #if the length is less than the best length stored
            best = sa_output.cost
            found = i
            best_route = sa_output.path
    

    # Plotting the path
    path = best_route
    x = [tsp_input.coordinates[i][0] for i in path]
    y = [tsp_input.coordinates[i][1] for i in path]
    axs[0, 0].plot(x, y, marker='o')
    axs[0, 0].set_title("Path")

    # Plotting cost graph
    axs[0, 1].plot(costs, color='blue')
    axs[0, 1].set_title("Cost over Iterations")

    # Plotting temperature graph
    axs[1, 0].plot(temperatures, color='red')
    axs[1, 0].set_title("Temperature over Iterations")

    # Plotting probability graph as dots
    axs[1, 1].scatter(range(len(probabilities)), probabilities, color='green')
    axs[1, 1].set_title("Acceptance Probability")

    # Draw the plots
    plt.draw()

    plt.show()
"""
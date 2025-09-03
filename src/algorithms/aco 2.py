from random import randint, random
from algorithms.common import *

class Graph():
    def __init__(self, n, dist): #n - number of cities, dist - distance matrix

        if n==0: # check if any cities are given
            return "No cities are given"
        if n!=len(dist) or n!=len(dist[0]): #check if the size of matrix is correct
            return "The size of the distance matrix isn't correct"


        self.n = n
        max_d = 0 #maximum distance
        self.pheromone = []
        self.heuristic = []
        self.dist = dist
        self.update = []        
        for i in range(n):
            self.pheromone.append([])
            self.update.append([])
            for j in range(n):   
                if i == j:   dist[i][j] = inf
                if dist[i][j]>max_d:     max_d = dist[i][j]; #find max distance
                self.pheromone[i].append(1) #at first, pheromones are equal to 1
                if i == j:  self.pheromone[i][j] = 0
                
                self.update[i].append(0)

        for i in range(n):
            self.heuristic.append([])
            for j in range(n):
                self.heuristic[i].append(max_d/dist[i][j]) #heuristic value of edge is max distance / length od edge
                # heuristic value - attractiveness of edge, the bigger is distance, less attractive the edge is
                if i==j:     self.heuristic[i][j] = 0
                if dist[i][j] == 0:  self.heuristic[i][j] = 0; #to avoid inf heuristic


    def choose_first_city(self):
        return randint(0, self.n-1)
    
    def choose_next_city(self, route, used, parameters):
        l = len(route)
        last_city = route[-1]
        probabilities = []
        sum_probabilities = 0

        if l == self.n:
            return -1; #if there are no available vertices, path is finished, so return -1

        for i in range(self.n):
            
            #if we already used an edge, its probability is 0
            if i in used:
                probability = 0
            else:
                #probability of edge is pheromone^alpha * heuristic*beta
                probability = pow(self.pheromone[last_city][i], parameters.alpha) * pow(self.heuristic[last_city][i], parameters.beta)
                
            probabilities.append(probability)
            sum_probabilities += probability

        if sum_probabilities==0: #if all probabilities are 0, just choose any node that hasn't been used yet
            for i in range(self.n):
                if not i in used:
                    return i
        
        for i in range(self.n):
            probabilities[i] = probabilities[i] * 1.0 / sum_probabilities #divide all probabilities by their total
            #so that the sum of all probabilities is 1
        
        
        random_n = random() #generate random number in range [0,1)
        
        #find in which range the random_n lies and return the vertex number
        for i in range(self.n):
            if i in used:   continue #don't consider vertices that are already used
            random_n -= probabilities[i]; 
            if random_n<=0: return i
            
        return -1 # if nothing found, return -1
    

    def path_length(self, path): #simple function for finding the path length
        length = 0
        for i in range (1, len(path)):
            length += self.dist[path[i-1]][path[i]] #sum up the distances between consecutive nodes
        return length
    
    def update_pheromone_levels(self, parameters): #update pheromone levels (after each iteration)
        for i in range(self.n):
            for j in range(self.n):
                self.pheromone[i][j] = (1-parameters.evaporation_rate)*self.pheromone[i][j] #decrease by percentage dictated by evaporation rate
                self.pheromone[i][j] += self.update[i][j] #add the update (delta tau sum)
      
      
    def clear_update(self): #set update to 0
        for i in range(self.n):
            for j in range(self.n):
                self.update[i][j] = 0
      
        
    def shake_pheromones(self): #optional function that is executed when the best route is improved
        #sets value of pheromone for all edges to the mean of all pheromone values
        total_pheromone = 0
        
        for i in range(self.n):
            for j in range(self.n):
                total_pheromone += self.pheromone[i][j]
                
        mean = total_pheromone/(self.n*(self.n-1))
        for i in range(self.n):
            for j in range(self.n):
                self.pheromone[i][j] = mean



class Ant():
    
    def __init__(self, ant_number):
        self.k = ant_number
        self.path_length = 0
        self.path = []
        
    def construct_path(self, graph, parameters):
        next_city = graph.choose_first_city() #choose first city
        self.path.clear()
        used = []
        while next_city!=-1: #while it's possible to choose another node
            self.path.append(next_city) #add current node to the path
            used.append(next_city) 
            next_city = graph.choose_next_city(self.path, used, parameters) #choose the next node randomly using the probabilstic function
        
        self.path.append(self.path[0]) #path has to be a cycle, so add the first city to the end
        self.path_length = graph.path_length(self.path)


class ACO():
    def __init__(self, tsp_input, parameters):
        self.n_ants = parameters.n_ants
        self.ants = []        
        for ant in range(self.n_ants):
            self.ants.append(Ant(ant)) #create artificial ants :) my favourite part
            
        self.graph = Graph(tsp_input.n, tsp_input.dist)
        self.parameters = parameters

    def construct_paths(self): #construct path for each ant
        for i in range(len(self.ants)):
            self.ants[i].construct_path(self.graph, self.parameters)
      
    def compare_edges(self): #calculate update (sum of delta tau) for each edge
        self.graph.clear_update()
        for k in range(len(self.ants)):
            ant = self.ants[k]
            for i in range(1, len(ant.path)):
                self.graph.update[ant.path[i-1]][ant.path[i]] += self.parameters.Q / ant.path_length; 
          
    def iteration(self):
        self.construct_paths() #construct path for each ant
        self.compare_edges() #create an update
        self.graph.update_pheromone_levels(self.parameters) #update pheromone levels

        #the rest of this function is creating the output
        #OBJECTIVE 2.3 - return data after each iteration
        best_length = inf
        best_route = []
        ant_route = []
        
        for k in range(len(self.ants)):
            ant = self.ants[k]
            if ant.path_length < best_length:
                best_length = ant.path_length
                best_route = ant.path
            ant_route.append(ant.path)
            
        output = ACO_output(self.graph.n, self.parameters.n_ants, [], best_route, [], best_length)
        return output

    def shake(self): #shake function
        self.graph.shake_pheromones()



def solve_aco(input, parameters):
    aco = ACO(input, parameters)
    
    best = inf
    best_found = 0
    output = []

    for iteration in range(parameters.iterations):
        iteration_output = aco.iteration()
        output.append(iteration_output)

        if iteration_output.cost < best: #if the length is less than the best length stored#
            #update the best solution
            best = iteration_output.cost
            best_found = iteration
        
        
    return best_found, output
    
    
    
    

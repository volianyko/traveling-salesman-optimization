#include <bits/stdc++.h>
using namespace std;

//#include "common.h"
//#include "held-karp.cpp"

class Graph{
    public:
        int n;
        float dist[max_n][max_n], heuristic[max_n][max_n], pheromone[max_n][max_n];
        float update[max_n][max_n];
        Graph(tsp_input input) { //graph initialization
            n = input.n;
            float max_d = 0; //maximum distance
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {   
                    if (i == j) input.dist[i][j] = inf;
                    dist[i][j] = input.dist[i][j]; 
                    if(dist[i][j]>max_d) max_d = dist[i][j]; //find max distance
                    pheromone[i][j] = 1; //at first, pheromones are equal to 1
                    if (i == j) pheromone[i][j] = 0;
                }
            }
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    heuristic[i][j] = max_d/dist[i][j]; //heuristic value of edge is max distance / length od edge
                    //heuristic value - attractiveness of edge, the bigger is distance, less attractive the edge is
                    if(i==j) heuristic[i][j] = 0;
                    if(dist[i][j] == 0) heuristic[i][j] = 0; //to avoid inf heuristic
                }
            }
        }

        int choose_first_city(){
            return random()%n; //random city from 0 to n-1
        }
        int choose_next_city(vector<int> route, set<int> used, aco_input parameters){
            int l = route.size(); 
            int last_city = route[l-1]; //find last city
            vector<float> probabilities; //vector of probibily functions of neighbours
            float sum_probabilities = 0; 

            if(route.size() == n) return -1; //if there are no available vertices, path is finished, so return -1

            for(int i=0;i<n;i++){
                //probability of edge is pheromone^alpha * heuristic*beta
                //this value is multiplied by 1-used.count(1) so that if we already used an edge, its probability is 0
                float probability = (1-used.count(i)) * pow(pheromone[last_city][i], parameters.alpha) * pow(heuristic[last_city][i], parameters.beta);
                probabilities.push_back(probability);
                sum_probabilities += probability;
            }
            if (sum_probabilities==0){ //if all probabilities are 0, just choose any node that hasn't been used yet
                for(int i=0;i<n;i++){
                    if(used.count(i)==0) return i;
                }
            }
            for(int i=0;i<n;i++){
                probabilities[i] = probabilities[i] * 1.0 / sum_probabilities; //divide all probabilities by their total
                //so that the sum of all probabilities is 1
            }
            float random_n = (float) rand()/RAND_MAX; //generate random number in range [0,1]
            
            //find in which range the random_n lies and return the vertex number
            for(int i=0;i<n;i++){
                if(used.count(i)!=0) continue; //don't consider vertices that are already used
                random_n -= probabilities[i]; 
                if(random_n<=0) return i;
            }
            return -1; // if nothing found, return -1
        }

        float path_length(vector<int> path){ //simple function for finding the path length
            float length = 0;
            for(int i=1;i<path.size();i++){
                length += dist[path[i-1]][path[i]]; //sum up the distances between consecutive nodes
            }
            return length;
        }
        void update_pheromone_levels(aco_input parameters){ //update pheromone levels (after each iteration)
            for(int i=0; i<n; i++){
                for(int j=0; j<n; j++){
                    pheromone[i][j] = (1-parameters.evaporation_rate)*pheromone[i][j]; //decrease by percentage dictated by evaporation rate
                    pheromone[i][j] += update[i][j]; //add the update (delta tau sum)
                }
            }
        }
        void clear_update(){ //set update to 0
            for(int i=0; i<n; i++){
                for(int j=0; j<n; j++){
                    update[i][j] = 0;
                }
            }
        }
        void shake_pheromones(){ //optional function that is executed when the best route is improved
            //pheromone = mean of pheromones
            float total_pheromone = 0;
            for(int i=0; i<n; i++){
                for(int j=0; j<n; j++){
                    total_pheromone += pheromone[i][j];
                }
            }
            float mean = total_pheromone/=(n*(n-1));
            for(int i=0; i<n; i++){
                for(int j=0; j<n; j++){
                    pheromone[i][j] = mean;
                }
            }
        }

};



class Ant {
    public:
        int k;
        float path_length;
        vector<int> path;
        Ant(int ant_number){
            k = ant_number; // unique ant number
        }
        void construct_path(Graph graph, aco_input parameters){
            int next_city = graph.choose_first_city(); //choose first city
            path.clear();
            set<int> used;
            while(next_city!=-1){ //while it's possible to choose another node
                path.push_back(next_city); //add current node to the path
                used.insert(next_city);
                next_city = graph.choose_next_city(path, used, parameters); //choose the next node randomly using the probabilstic function
            }
            path.push_back(path[0]); // path has to be a cycle, so add the first city to the end
            path_length = graph.path_length(path); //
        }
};


class ACO {
    public:
        Graph graph; //graph has distance, pheromones, heuristic matrices
        aco_input parameters; // aco parameters
        vector<Ant> ants; //vector of ants
        float update[max_n][max_n]; //sum of delta tau for each edge

        ACO(tsp_input input, aco_input parameters) : graph(input), parameters(parameters) {
            int n_ants = parameters.n_ants;
            for(int ant=0; ant<n_ants; ant++){
                ants.push_back(Ant(ant)); //create artificial ants :) my favourite part
            }
        }
        void construct_paths(){ //construct path for each ant
            for(int i=0; i<ants.size(); i++){
                ants[i].construct_path(graph, parameters);
            }
        }
        void compare_edges(){ // calculate update (sum of delta tau) for each edge
            graph.clear_update();
            for(int k=0; k<ants.size(); k++){
                auto ant = ants[k];
                for(int i=1; i<ant.path.size(); i++){
                    //cout<<ant.path[i-1]<<" "<<ant.path[i]<<" "<<ant.path_length<<" "<<graph.update[ant.path[i-1]][ant.path[i]]<<endl;
                    graph.update[ant.path[i-1]][ant.path[i]] += parameters.Q / ant.path_length; 
                }
            }

        }
        aco_output iteration(){
            construct_paths(); //construct path for each ant
            compare_edges(); //create update
            graph.update_pheromone_levels(parameters); //update pheromone levels

            //the rest of this function is creating the output
            aco_output output;
            float best_length = inf;
            vector<int> best_route;

            for(int k=0; k<ants.size(); k++){
                auto ant = ants[k];
                if(ant.path_length < best_length){
                    best_length = ant.path_length;
                    best_route = ant.path;
                }
                for(int i=0; i<ant.path.size(); i++){
                    output.ant_route[k].push_back(ant.path[i]);
                }
            }
            for(int i=0; i<graph.n; i++){
                for(int j=0; j<graph.n; j++){
                    output.pheromone[i][j] = graph.pheromone[i][j];
                }
            }
            output.best_route = best_route;
            output.length = best_length;
            output.n = graph.n;
            output.n_ants = parameters.n_ants;
            return output;

        }   
        void shake(){ //shake function
            graph.shake_pheromones();
        }
};

void print_aco_output(aco_output output){ //function for local testing
    //outputs results of each iteration
    cout<<"Best length: "<<output.length<<endl;
    cout<<"Best route: ";
    for(int i=0;i<output.best_route.size();i++) cout<<output.best_route[i]<<" ";
    cout<<endl;
    /*
    cout<<"Pheromones:"<<endl;
    for(int i=0;i<output.n;i++){
        for(int j=0;j<output.n;j++){
            cout<<output.pheromone[i][j]<<" ";
        }
        cout<<endl;
    }
    for(int i=0;i<output.n_ants;i++){
        cout<<"Ant "<<i<<endl;
        for(int j=0;j<output.ant_route[i].size();j++){
            cout<<output.ant_route[i][j]<<" ";
        }
        cout<<endl;
    }*/
}


void solve_aco(tsp_input input, aco_input p) {
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0); //for faster runtime

    vector<float> best_routes; //best route of every iteration
    ACO aco = ACO(input, p);
    float best = inf; //shortest length
    int found = 0; //iteration at which this length was found
    vector<int> best_route; //route with the shortest length

    for(int i=1;i<=p.iterations;i++){

        //cout<<endl<<endl<<"Iteration "<<i<<endl;
        aco_output out = aco.iteration(); //do iteration of aco
        best_routes.push_back(out.length); 

        if(out.length<best){ //if the length is less than the best length stored
            best = out.length;
            found = i;
            best_route = out.best_route;
            if(p.shake) aco.shake(); //optional shake function
        }
        //print_aco_output(out); //print output (for local testing)
    }


    cout<<"ACO best: "<<best<<" found:"<<found<<endl;

    cout<<"Route: ";
    for(int i=0;i<best_route.size();i++){
        cout<<best_route[i]<<" ";
    }
    cout<<endl;
    
}

//g++ -o main main.cpp Graph.cpp Ant.cpp ACO.cpp

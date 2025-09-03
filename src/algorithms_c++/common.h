#define inf 1000000
#define max_n 100
#define max_n_ants 100
#define max_dist 100

using namespace std;



struct tsp_input{
    int n; //number of cities
    float dist[max_n][max_n]; //adjacency matrix
};

struct tsp_output{
    int min_dist; //length of the shortest tsp path
    vector<int> shortest_path; //list of citites in the shortest paths
};

struct aco_input{
    float alpha, beta, Q, evaporation_rate;
    int n_ants, iterations;
    bool shake;
};

struct aco_output{
    int n, n_ants;
    vector<int> ant_route[max_n_ants];
    vector<int> best_route;
    float length, pheromone[max_n][max_n];
};

int binary_pow(int n, int p){ //faster way to raise a number to a power
    if(p==0) return 1;
    int x = binary_pow(n, p/2);
    if(p%2==0) return x*x;
    return x*x*n;
}
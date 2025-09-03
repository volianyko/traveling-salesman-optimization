#include <iostream>
using namespace std;

//change type to float later (think about how to deal with overfloaw)

int held_karp(tsp_input input){
    int n = input.n;
    auto dist = input.dist;

    int dp[1<<n][max_n]; //Set S is represented as a binary number of length n where 1 at position x corresponds to including city x

    memset(dp, inf, sizeof(dp)); //set all dp elements to infinity
    for(int mask=1; mask<(1<<n); mask++){ 
        for(int v=1; v<n; v++){
            dp[mask][v] = inf;
        }
    }
    dp[1][0] = 0; //distance from 1 to 1 is 0

    for(int mask=1; mask<(1<<n); mask++){ //mask represents a set S
        //cout<<mask<<endl;
        for(int v=1; v<n; v++){
            for(int u=0; u<n; u++){
                /* 1<<v is left shift of 1, v bits (the same as 2 to the power of v)
                   mask & (1<<v) is 0 if mask has 0 at position v -> so S doesn't contain v
                   mask & (1<<v) is 1 if mask has 1 at position v -> so S contains v */
                if (u==v || !(mask & (1<<v)) || !(mask & (1<<u))) continue; //S has to contain v and u
                // ^ is xor, so mask ^ (1<<v) is S\v
                if (dist[u][v] != -1){
                    //int x = mask ^ (1<<v);
                    //cout<<"  "<<x<<" "<<u<<" "<<dist[u][v]<<endl;
                    if(dp[mask][v] > dp[mask ^ (1<<v)][u] + dist[u][v]) dp[mask][v] = dp[mask ^ (1<<v)][u] + dist[u][v];
                }
            }
            //if(mask & (1<<v)) cout<<" "<<v<<" "<<dp[mask][v]<<endl;
        }
    }
    int mask = (1<<n)-1; //represents set S = {1,2,3,...,n}
    int min_dist = inf;
    for(int v=1;v<n;v++){
        if (dist[v][0] != -1 && min_dist > dp[mask][v] + dist[v][0]) min_dist = dp[mask][v] + dist[v][0];
    }
    return min_dist;

}

/*
int main() {
    ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0); //for faster runtime

    int n, a[50][50];

    tsp_input input;
    

    cin>>n;
    input.n = n; 
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin>>input.dist[i][j];
        }
    }

    cout<<held_karp(input)<<endl;
    

    return 0;
}*/
from algorithms.common import *


def held_karp(input):
    n = input.n
    dist = input.dist

    if n>max_n:
        return heldkarp_output(0, [])

    dp = [[inf] * max_n for _ in range(1 << n)]  # Set S is represented as a binary number of length n where 1 at position x corresponds to including city x
    path = [[-1] * max_n for _ in range(1 << n)]  # To store the path information


    for mask in range(1, 1 << n): #set all elements of dp array to infinity
        for v in range(1, n):
            dp[mask][v] = inf

    dp[1][0] = 0  # distance from 1 to 1 is 0

    for mask in range(1, 1 << n):  # mask represents a set S
        for v in range(1, n):
            for u in range(n):
                #1<<v is left shift of 1, v bits (the same as 2 to the power of v)
                #mask & (1<<v) is 0 if mask has 0 at position v -> so S doesn't contain v
                #mask & (1<<v) is 1 if mask has 1 at position v -> so S contains v
                if u == v or not (mask & (1 << v)) or not (mask & (1 << u)):
                    continue  # S has to contain v and u
                if dist[u][v] != -1:
                    # ^ is xor, so mask ^ (1<<v) is S\v
                    if dp[mask][v] > dp[mask ^ (1 << v)][u] + dist[u][v]:
                        dp[mask][v] = dp[mask ^ (1 << v)][u] + dist[u][v]
                        path[mask][v] = u

    mask = (1 << n) - 1  # represents set S = {1,2,3,...,n}
    min_dist = inf
    end_vertex = -1 #this is needed to than reconstruct the optimal path

    for v in range(1, n):
        #find the minimum distance among all dp values
        if dist[v][0] != -1 and min_dist > dp[mask][v] + dist[v][0]:
            min_dist = dp[mask][v] + dist[v][0]
            end_vertex = v 

    # reconstruct the path
    path_list = []
    while mask > 0 and end_vertex!=-1:
        path_list.append(end_vertex)
        u = path[mask][end_vertex]
        mask ^= (1 << end_vertex)
        end_vertex = u

    path_list.append(path_list[0])
    return heldkarp_output(min_dist, path_list)
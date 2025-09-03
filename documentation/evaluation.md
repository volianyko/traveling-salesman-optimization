# Evaluation

Below is the list of objectives, and for each a verdict (whether it was hit) and a location where proof can be found.

| Objective | Description                                          | Was hit? | Where?                             |
| --------- | ---------------------------------------------------- | -------- | ---------------------------------- |
| 1         | explore maths behind aco, sa, and an exact algorithm | yes      | documented design -> algorithms    |
| 2.1       | aco constructs a valid route that is a tsp solution  | yes      | testing -> ACO -> results          |
| 2.2       | aco has input parameters                             | yes      | technical solution -> common.py    |
| 2.3       | aco returns data about every iteration               | yes      | technical solution -> aco.py       |
| 2.4       | aco is quick, efficient, and accurate                | yes      | testing -> ACO -> results          |
| 3.1       | sa constructs a valid route that is a tsp solution   | yes      | testing -> SA -> results           |
| 3.2       | sa has input parameters                              | yes      | technical solution -> common.py    |
| 3.3       | sa returns data about every iteration                | yes      | technical solution -> sa.py        |
| 3.4       | sa is quick, efficient, and accurate                 | yes      | testing -> SA -> results           |
| 4.1       | exact algorithm constructs the best possible route   | yes      | testing -> HK -> results           |
| 4.2       | exact algorithm return the route and its cost        | yes      | technical solution -> held_karp.py |
| 4.3       | exact algorithm is efficient and fast                | yes      | testing -> HK -> results           |
| 5         | create a visualisation                               | yes      | testing -> UI                      |
| 6         | link back-end and front-end                          | yes      | technical solution -> app.py       |

<div style="page-break-after: always;"></div>


As a result, all of the objectives were hit. I ended up doing a bit more functionality on the website than I aimed for in the first place which made it even easier to use. I've loved doing this project because I got to explore and learn a lot of maths that is behind the algorithms and TSP, and compare how the algorithms perfrom on TSP. I can say that I fulfilled my curiosity for the topic and am very happy with the result. 

Other people who used the visualisation are saying that it's simple, easy to understand and to use, and looks cool, so I think it's a success. 

TSP turned out to be a perfect problem to visually learn how meta-heuristics work and to compare their performance. So in the future, I'm planning to continue adding new algorithms such as Genetic Algorithm, Particle Swarm and others to the website. Hopefully not only to fulfill my personal curiosity, but also to share this tool wih others.

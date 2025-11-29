from Graph import create_grid_graph, print_grid_graph, terrain_cost
from algorithms import bfs,bfs_shortest_path, dijkstra, shortest_path
g = create_grid_graph(20,10, terrain_cost,seed=101,wall_probability=0.4)


u = (9,0)
v = (1,19)



path, cost = shortest_path(g,v,u)


print_grid_graph(g)
print('\n')
print_grid_graph(g,path)
print(cost, path)

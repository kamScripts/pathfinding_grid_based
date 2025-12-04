import cProfile
from Graph import create_grid_graph, print_grid_graph
from algorithms import shortest_path

g = create_grid_graph(20,20,seed=36991)


u = (0,0)
v = (1,15)
path_d,cost_d=shortest_path(g,u,v,'dijkstra')
path_A, cost_A=shortest_path(g,u,v,'astar')
print_grid_graph(g)
print_grid_graph(g,path_d)
print('A* -> ',cost_A,' Dijkstra -> ',cost_d)
print(path_d,path_A)

#g=create_grid_graph(500,500)
#u=(0,0)
#v=(497,497)
#cProfile.runctx('shortest_path(g,u,v, algorithm="astar")',
#            globals(), locals(), sort='cumulative')


import cProfile
from Graph import create_grid_graph, print_grid_graph
from algorithms import shortest_path, a_star, reconstruct_path

g = create_grid_graph(5000,5000,seed=36991)


u = (0,0)
v = (4400,4861)
path_2,cost2=shortest_path(g,u,v)
previous, g_score = a_star(g,u,v)
path = reconstruct_path(g_score, previous,u,v)
#print_grid_graph(g,path)
print('A* -> ',g_score[v],' Dijkstra -> ',cost2)
#print_grid_graph(g,path_2)

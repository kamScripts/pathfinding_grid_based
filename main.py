from Graph import create_grid_graph, print_grid_graph, terrain_cost
from algorithms import dfs, construct_path
g = create_grid_graph(10,10, terrain_cost)
visited = {}
dfs(g,(0,0), visited)

u = (3,1)
v = (9,1)
path = construct_path(u,v,visited,g)
print_grid_graph(g,path)





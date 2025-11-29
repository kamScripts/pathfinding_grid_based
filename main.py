from Graph import create_grid_graph, print_grid_graph, terrain_cost
from algorithms import dfs, construct_path, dijkstra, shortest_path
g = create_grid_graph(5,5, terrain_cost)
g.remove_edge((1,2),(2,2))
visited = {}
dfs(g,(0,0), visited)

u = (4,0)
v = (0,4)

path, cost = shortest_path(g,v,u)


print_grid_graph(g)
print(cost, path)
print_grid_graph(g,path)











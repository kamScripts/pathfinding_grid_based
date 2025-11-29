from Graph import create_grid_graph, print_grid_graph, terrain_cost
from algorithms import dfs, construct_path, dijkstra, shortest_path
g = create_grid_graph(5,5, terrain_cost)
visited = {}
dfs(g,(0,0), visited)

u = (1,4)
v = (1,0)


distances,previous = dijkstra(g, u,v)
path, cost = shortest_path(g,v,u)

print(cost, path)
print_grid_graph(g,path)
print_grid_graph(g)










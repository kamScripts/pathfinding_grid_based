from Graph import create_grid_graph, print_grid_graph, terrain_cost
from algorithms import bfs,bfs_shortest_path, dijkstra, shortest_path
g = create_grid_graph(30,10, terrain_cost)
g.remove_edge((1,2),(2,2))

g.remove_edge((1,3),(2,3))
g.disconnect_node((0,10))
g.disconnect_node((1,15))
g.disconnect_node((5,23))
g.disconnect_node((7,23))


u = (1,4)
v = (9,23)



path, cost = shortest_path(g,v,u)
bfs_path= bfs_shortest_path(g,u,v)

print_grid_graph(g,bfs_path)
print(cost, path)
print_grid_graph(g,path)











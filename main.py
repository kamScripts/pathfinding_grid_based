from Graph import create_grid_graph, print_grid_graph
from algorithms import bfs,bfs_shortest_path, dijkstra, shortest_path

g = create_grid_graph(45,5)


u = (0,0)
v = (44,4)



path, cost = shortest_path(g,v,u)


#print_grid_graph(g)
#print('\n')
print_grid_graph(g,path)

print(f'total cost: {cost}')
for vertex, cost in path:
    print(vertex,cost,sep=', ', end=' => ')

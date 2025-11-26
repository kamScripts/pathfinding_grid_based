from Graph import create_grid_graph, print_grid_graph, terrain_cost

g = create_grid_graph(20,10, terrain_cost)
print_grid_graph(g,[(0,0),(0,1),(0,2),(0,3)])

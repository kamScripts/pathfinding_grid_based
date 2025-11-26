def dfs(graph, start_coords: tuple[int, int], visited: dict[tuple[int, int], tuple[int, int]]):
    """
    Depth-First Search on your Graph implementation.
    Uses a dictionary for visited nodes.

    Parameters
    ----------
    graph : Graph
        The graph instance.
    start_coords : tuple[int, int]
        Coordinates of the starting node.
    visited : dict
        Dictionary of visited nodes. Keys are coordinates,
        values can store node data (here: coordinates again).
    """
    if start_coords in visited:
        return

    # Mark as visited
    visited[start_coords] = graph.node_at(start_coords)

    node = graph.node_at(start_coords)
    if not node:
        return

    # Recurse on neighbors
    for neighbor_node, weight in node.neighbours.items():
        neighbor_coords = neighbor_node.get_coords()
        if neighbor_coords not in visited:
            dfs(graph, neighbor_coords, visited)
def construct_path(u,v, visited, graph):
    path=[]
    if v in visited:
        path.append(v)
        walk = v
        while walk != u:
            e = visited.get(walk)
            for n in e.neighbours:
                c = n.get_coords()
                if c not in path:
                    walk = c
                    path.append(walk)
                    break
            print(walk == u)
    
    path.reverse()
    return path
    

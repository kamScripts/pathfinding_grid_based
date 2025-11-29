from heapq import heapify, heappop, heappush
from typing import Dict, Tuple, Optional, List
from Graph import Graph

def dijkstra(
    graph: Graph,
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[Optional[Dict[Tuple[int, int], float]], Dict[Tuple[int, int], Tuple[int, int]]]:
    """
    Run Dijkstra's algorithm on the graph from start to goal.
    """
    if not graph.node_at(start):
        raise ValueError(f"Start node {start} does not exist in graph")
    if not graph.node_at(goal):
        raise ValueError(f"Goal node {goal} does not exist in graph")

    # Priority queue: (distance, coords)
    pq = [(0, start)]
    heapify(pq) # make pq a Priority Queue.
    distances: Dict[Tuple[int, int], float] = {start: 0}
    previous: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while pq:
        current_dist, current = heappop(pq)

        if current == goal:
            break

        if current_dist > distances.get(current, float('inf')):
            continue

        node = graph.node_at(current)
        for neighbor_node, weight in node.neighbours.items():
            neighbor_coords = neighbor_node.get_coords()
            new_dist = current_dist + weight

            if new_dist < distances.get(neighbor_coords, float('inf')):
                distances[neighbor_coords] = new_dist
                previous[neighbor_coords] = current
                heappush(pq, (new_dist, neighbor_coords))
        

    return distances, previous
def shortest_path(graph: Graph, start: tuple, goal: tuple)->tuple[List,float]:
    """
    Returns (path, cost) or (None, None) if no path exists.
    """
    distances, previous = dijkstra(graph, start, goal)
    
    if goal not in distances:
        return None, None  # unreachable
    
    path = reconstruct_path(previous, start, goal)
    cost = distances[goal]
    
    return path, cost

def reconstruct_path(
    previous: Dict[Tuple[int, int], Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Reconstruct the shortest path from start to goal using the previous dictionary.
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous.get(current)
    else:
        return []  # start not reached
    return path[::-1]
def dfs(graph, start_coords: tuple[int, int], visited: dict[tuple[int, int], tuple[int, int]]):
    """
    Depth-First Search on your Graph implementation.
    Uses a dictionary for visited nodes.
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
 
    path.reverse()
    return path
    

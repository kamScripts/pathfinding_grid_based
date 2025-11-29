from heapq import heapify, heappop, heappush
from typing import Dict, Tuple, Optional, List
from Graph import Graph

def dijkstra(
    graph: Graph,
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], Tuple[int, int]]]:
    """
    Dijkstra's algorithm using priority queue (heapq).
    Returns:
        - distances: best known distance from start to each node
        - previous: parent pointer for path reconstruction
    """

    if graph.node_at(start) is None:
        raise ValueError(f"Start node {start} does not exist in the graph")
    if graph.node_at(goal) is None:
        raise ValueError(f"Goal node {goal} does not exist in the graph")


    # pq - Priority queue: stores (distance, coordinates)
    # heapq ensures we always expand the current shortest path first
    pq: List[Tuple[float, Tuple[int, int]]] = []
    heappush(pq, (0, start))

    # distances: best known distance from start to each node
    distances: Dict[Tuple[int, int], float] = {start: 0}
    # {} to reconstruct the final path (parent map)
    previous: Dict[Tuple[int, int], Tuple[int, int]] = {}
    # Set to avoid visiting same nodes
    visited: set[Tuple[int, int]] = set()

    while pq:
        # Pop the node with the smallest known distance
        current_dist, current = heappop(pq)
        # Skip if visited
        if current in visited:
            continue

        # Mark as visited, to prevent re-visiting
        visited.add(current)

        # Goal reached with shortest path
        if current == goal:
            break

        # Explore all neighbors
        for neighbor_coords, weight in graph.neighbours(current):
            neighbor = neighbor_coords

            # Skip already visited nodes
            if neighbor in visited:
                continue

            # Relaxation step:
            new_dist = current_dist + weight

            if new_dist < distances.get(neighbor, float('inf')):
                # Update best known distance and parent
                distances[neighbor] = new_dist
                previous[neighbor] = current

                # Push the newly discovered path into priority queue
                heappush(pq, (new_dist, neighbor))

    return distances, previous
def shortest_path(
    graph: Graph,
    start: tuple[int,int],
    goal: tuple[int,int]
) -> tuple[List[tuple[int,int]], float] | tuple[None, None]:
    """
    Returns (path, cost) or (None, None) if no path exists.
    """
    distances, previous = dijkstra(graph, start, goal)

    if goal not in distances:
        return None, None

    path: List[tuple[int,int]] = [goal]
    current = goal
    while current in previous:
        current = previous[current]
        path.append(current)

    cost = distances[goal]

    return path[::-1], cost


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
    

from collections import deque
from heapq import heappop, heappush
from typing import Dict, Tuple, List
from Graph import Graph


def dijkstra(
    graph: Graph, start: Tuple[int, int], goal: Tuple[int, int]
) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], Tuple[int, int]]]:
    """
    Dijkstra's algorithm using a priority queue (heapq).
    Explores nodes in order of increasing distance from start.
    Guaranteed to find the shortest path in graphs with non-negative weights.
    Returns:
        distances = best known distance from start to each reachable node
        previous = parent map for path reconstruction
    """

    if not graph.node_at(start):
        raise ValueError(f"Start {start} out of bounds")
    if not graph.node_at(goal):
        raise ValueError(f"Goal {goal} out of bounds")

    # pq - Priority queue: stores (distance, coordinates)
    pq: List[Tuple[float, Tuple[int, int]]] = []
    heappush(pq, (0, start))

    # distances: best known distance from start to each node
    distances: Dict[Tuple[int, int], float] = {start: 0}
    # previous: to reconstruct the final path (parent map)
    previous: Dict[Tuple[int, int], Tuple[int, int]] = {}
    # visited: to avoid visiting same nodes
    visited: set[Tuple[int, int]] = set()

    while pq:
        # Pop the node with the smallest known distance
        current_dist, current = heappop(pq)
        # Skip if visited
        if current in visited:
            continue
        # Mark as visited, to prevent revisiting
        visited.add(current)

        # Goal reached with shortest path
        if current == goal:
            break

        # Explore all neighbours
        for neighbour_coords, weight in graph.neighbours(current):
            neighbour = neighbour_coords

            # Skip already visited nodes
            if neighbour in visited:
                continue

            # Relaxation step
            new_dist = current_dist + weight

            if new_dist < distances.get(neighbour, float("inf")):
                # Update best known distance and parent
                distances[neighbour] = new_dist
                previous[neighbour] = current

                # Push the newly discovered path into priority queue
                heappush(pq, (new_dist, neighbour))

    return distances, previous


def a_star(
    graph: Graph, start: tuple[int,int],
    goal:tuple[int,int]
    ) -> tuple[dict[tuple[int,int], tuple[int,int]], dict[tuple[int, int], float]]:
    """
    A* path search algorithm using a priority queue (heapq).
    Returns:
        previous  - parent pointer map for reconstructing the path
        g_score   - exact cost from start to each visited node
    """
    def heuristic(node):
        """Heuristic estimate from start to the goal,
        using Manhattan distance for grid based maps."""
        return 1.5*(abs(node[0] - goal[0]) + abs(node[1] - goal[1]))

    pq = []
    # tie-breaking - prevents a bug when two vertices have the same f_score
    counter = 0
    heappush(pq, (heuristic(start), counter, start)) # (f_score, tie-breaker counter, vertex)
    counter += 1

    open_set = {start}
    g_score = {start: 0.0}
    previous = {}

    while pq:
        _, _, current = heappop(pq) # discovery vertex
        if current not in open_set:
            continue
        
        open_set.remove(current)

        if current == goal: # end loop if goal found
            return previous, g_score

        for neighbour, cost in graph.neighbours(current):
            tentative_g = g_score[current] + cost

            if tentative_g < g_score.get(neighbour, float("inf")):
                # Better path to neighbour discovered
                previous[neighbour] = current
                g_score[neighbour] = tentative_g
                f_score = tentative_g + heuristic(neighbour)

                if neighbour not in open_set:
                    heappush(pq, (f_score, counter, neighbour))
                    open_set.add(neighbour)
                    counter += 1
    return previous, g_score


def shortest_path(
    graph: Graph, start: tuple[int, int], goal: tuple[int, int], algorithm="dijkstra"
) -> tuple[list[tuple[tuple[int, int], float]], float] | tuple[None, None]:
    """
    Prepare Path and total cost from start to the based on
    either Dijkstra or A* Search.
    Returns:
        List of (node, cumulative_cost) from start to the goal, and total cost
        None if no path exists
    """
    if algorithm == "dijkstra":
        distances, previous = dijkstra(graph, start, goal)
    elif algorithm == "astar":
        previous, distances = a_star(graph, start, goal)
    else:
        raise ValueError("Unknown algorithm")

    if goal not in distances:
        return None, None

    path = [(goal, distances[goal])]
    current = goal
    while current in previous:
        current = previous[current]
        path.append((current, distances[current]))

    return path[::-1], distances[goal]


def bfs(
    graph: Graph, start: tuple[int, int]
) -> Dict[tuple[int, int], tuple[int, int] | None]:
    """
    Breadth-First Search  best for unweighted or same-cost grids.
    Returns:
        parent map (previous dictionary) where previous[node] = parent.
    """

    previous: Dict[tuple[int, int], tuple[int, int] | None] = {}
    visited: Dict[tuple[int, int], bool] = {}
    queue = deque([start])

    visited[start] = True
    previous[start] = None  # start has no parent

    while queue:
        current = queue.popleft()

        for neighbour, _ in graph.neighbours(current):
            if neighbour not in visited:
                visited[neighbour] = True
                previous[neighbour] = current
                queue.append(neighbour)

    return previous


def bfs_shortest_path(graph: Graph, start, goal)->list[tuple[int,int]] | None:
    """
    Helper function that returns a list of coordinates
    from start to the goal on unweighted graph.
    """
    previous = bfs(graph, start)
    if goal not in previous:
        return None

    path: List[Tuple[int, int]] = []
    current = goal
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

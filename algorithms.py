from collections import deque
from heapq import heappop, heappush
from typing import Dict, Tuple, List
from Graph import Graph


def dijkstra(
    graph: Graph, start: Tuple[int, int], goal: Tuple[int, int]
) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], Tuple[int, int]]]:
    """
    Dijkstra's algorithm using priority queue (heapq).
    Returns
        distances: best known distance from start to each node
        previous: parent pointer for path reconstruction
    """

    if not graph.node_at(start):
        raise ValueError(f"Start {start} out of bounds")
    if not graph.node_at(goal):
        raise ValueError(f"Goal {goal} out of bounds")

    # pq - Priority queue: stores (distance, coordinates)
    # heapq ensures current expands shortest path first
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

            # Relaxation step:
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
    ) -> tuple[
        dict[tuple[int,int], tuple[int,int]], dict[tuple[int, int], float]
        ]:
    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_heap = []
    counter = 0
    heappush(open_heap, (heuristic(start), counter, start))
    counter += 1

    open_set = {start}
    g_score = {start: 0.0}
    previous = {}

    while open_heap:
        _, _, current = heappop(open_heap)
        if current in open_set:
            open_set.remove(current)
        else:
            continue

        if current == goal:
            return previous, g_score

        for neighbour, cost in graph.neighbours(current):
            tentative_g = g_score[current] + cost

            if tentative_g < g_score.get(neighbour, float("inf")):
                previous[neighbour] = current
                g_score[neighbour] = tentative_g
                f_score = tentative_g + heuristic(neighbour)

                if neighbour not in open_set:
                    heappush(open_heap, (f_score, counter, neighbour))
                    open_set.add(neighbour)
                    counter += 1
    return previous, g_score


def shortest_path(
    graph: Graph, start: tuple[int, int], goal: tuple[int, int], algorithm="dijkstra"
) -> tuple[list[tuple[tuple[int, int], float]], float] | tuple[None, None]:
    """
    Returns (path, cost) or (None, None) if no path exists.
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
    Breadth-First-Search.
    Returns previous dict where previous[node] = parent
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


def bfs_shortest_path(graph: Graph, start, goal):
    previous = bfs(graph, start)
    if goal not in previous:
        return None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = previous[current]
    return path[::-1]

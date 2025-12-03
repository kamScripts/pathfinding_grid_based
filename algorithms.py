from collections import  defaultdict, deque
from heapq import heappop, heappush
from typing import Dict, Tuple, List, Set
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

    if not graph.node_at(start):
        raise ValueError(f"Start {start} out of bounds")
    if not graph.node_at(goal):
        raise ValueError(f"Goal {goal} out of bounds")


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
) -> tuple[list[tuple[tuple[int, int], float]], float] | tuple[None, None]:
    """
    Returns (path, cost) or (None, None) if no path exists.
    """
    distances, previous = dijkstra(graph, start, goal)

    if goal not in distances:
        return None, None

    path = [(goal,distances[goal])]
    current = goal
    
    while current in previous:
        current = previous[current]
        path.append((current,distances[current]))

    cost = distances[goal]

    return path[::-1], cost
def a_star(
    graph,
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[Dict[Tuple[int, int], Tuple[int, int]], Dict[Tuple[int, int], float]]:
    """
    A* search with a priority queue
    """
    if not graph.node_at(start):
        raise ValueError(f"Start {start} out of bounds")
    if not graph.node_at(goal):
        raise ValueError(f"Goal {goal} out of bounds")
    def heuristic(node: Tuple[int, int]) -> float:
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        manhattan = dx + dy

        # tie-breaking
        dx1 = node[0] - goal[0]
        dy1 = node[1] - goal[1]
        dx2 = start[0] - goal[0]
        dy2 = start[1] - goal[1]
        cross = abs(dx1*dy2 - dx2*dy1)
        return manhattan + cross * 0.001

    # Heap: (f_score, counter, node) - counter prevents comparison errors
    open_heap: List[Tuple[float, int, Tuple[int, int]]] = []
    counter = 0
    heappush(open_heap, (heuristic(start), counter, start))
    counter += 1

    open_set: Set[Tuple[int, int]] = {start}
    closed_set: Set[Tuple[int, int]] = set()

    g_score: Dict[Tuple[int,int], float] = {start: 0.0}
    previous: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while open_heap:
        _, _, current = heappop(open_heap) # f_score, count, current.

        if current not in open_set: # prevent KeyError
            continue

        open_set.remove(current)

        if current == goal:
            return previous, g_score

        closed_set.add(current)

        for neighbor, move_cost in graph.neighbours(current):
            tentative_g = g_score[current] + move_cost

            if neighbor in open_set and tentative_g < g_score.get(neighbor, float('inf')):
                open_set.remove(neighbor)
            if neighbor in closed_set and tentative_g < g_score.get(neighbor, float('inf')):
                closed_set.remove(neighbor)

            if neighbor in closed_set:
                continue

            if tentative_g < g_score.get(neighbor, float('inf')):
                previous[neighbor] = current
                g_score[neighbor] = tentative_g
                f_new = tentative_g + heuristic(neighbor)

                if neighbor not in open_set and neighbor not in closed_set:
                    heappush(open_heap, (f_new, counter, neighbor))
                    open_set.add(neighbor)
                    counter += 1

    return previous, g_score

def reconstruct_path(g_score, previous: dict,start:dict[int,int], goal:dict[int,int]) -> list[Tuple[int, int]] | None:
    """
    Reconstruct path from goal to start using parent pointers.
    Returns list of coordinates: [] or None if no path.
    """
    if goal not in previous and start not in previous.values() and goal != start:
        return None

    path = []
    current = goal
    while current is not None:
        path.append((current, g_score[current]))
        current = previous.get(current)
    path.reverse()
    return path

def bfs(
    graph: Graph,
    start: tuple[int, int]
) -> Dict[tuple[int, int], tuple[int, int] | None]:
    """
    Breadth-First-Search.
    Returns: previous dict where previous[node] = parent
    """

    previous: Dict[tuple[int, int], tuple[int, int] | None] = {}
    visited: Dict[tuple[int, int], bool] = {}
    queue = deque([start])

    visited[start] = True
    previous[start] = None  # start has no parent

    while queue:
        current = queue.popleft()

        for neighbor, _ in graph.neighbours(current):  # ignore weight
            if neighbor not in visited:
                visited[neighbor] = True
                previous[neighbor] = current
                queue.append(neighbor)

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

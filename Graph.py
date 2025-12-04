import random
from typing import List, Tuple, Generator
# TODO: REPLACE  2D ADJACENCY LIST WITH 1D LIST
class Graph:
    """
    Ultra-fast 4-connected grid graph using 2D arrays.

    """
    # Directions: right and down only (to avoid duplicate edges)

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # Edge weights: weight[y][x][0=right, 1=down]
        self.weight: List[List[List[int]]] = [
            [[0, 0] for _ in range(width)]
            for _ in range(height)
        ]

    def node_at(self, coords: Tuple[int, int]) -> bool:
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbours(self, coords: Tuple[int, int]) -> Generator[Tuple[Tuple[int, int], int], None, None]:
        x, y = coords
        
        # Right
        if x + 1 < self.width and self.weight[y][x][0] > 0:
            yield (x + 1, y), self.weight[y][x][0]
            
        # Left
        if x > 0 and self.weight[y][x-1][0] > 0:
            yield (x - 1, y), self.weight[y][x-1][0]
        # Down
        if y + 1 < self.height and self.weight[y][x][1] > 0:
            yield (x, y + 1), self.weight[y][x][1]
        # Up
        if y > 0 and self.weight[y-1][x][1] > 0:
            yield (x, y - 1), self.weight[y-1][x][1]


def create_grid_graph(
    width: int, height: int,
    seed: int | str = 42,
    wall_probability: float = 0.10
) -> Graph:
    rnd = random.Random(seed)
    choice = rnd.choice
    rand = rnd.random
    COSTS = (1, 2, 3)

    g = Graph(width, height)

    for y in range(height):
        row = g.weight[y]
        for x in range(width):
            cell = row[x]
            if x + 1 < width and rand() >= wall_probability:
                cell[0] = choice(COSTS)
            if y + 1 < height and rand() >= wall_probability:
                cell[1] = choice(COSTS)

    return g

def cost_to_color(cost):

    if cost == 1:
        return "\033[38;5;41m"       # Dark gray -light gravel path
    if cost == 2:
        return "\033[38;5;63m"       # Green-medium forest
    if cost == 3:
        return "\033[38;5;198m"       # Yellow-rough / rocky
    return "\033[91m"

def print_grid_graph(g: Graph, path: list[tuple[int, int]] | None = None)->None:
    """
    CLI Graph Representation.
    Path edges and nodes in bright red.
    """
    path_set = set(coords for coords,_ in path) if path else set()
    width  = g.width
    height = g.height

    def is_path_edge(a: tuple[int,int], b:tuple[int,int]) -> bool:
        return a in path_set and b in path_set

    # Unicode constants
    H_LIGHT = "\u2500"   # ─ thin horizontal
    H_HEAVY = "\u2501"   # ━ bold horizontal (path)
    V_LIGHT = "\u2502"   # │ thin vertical
    V_HEAVY = "\u2503"   # ┃ bold vertical (path)

    NODE_EMPTY = "\u25CB"   # ○ open circle
    NODE_PATH  = "\u25CF"   # ● filled circle

    # Column headers
    header = "  "
    for col in range(width):
        header += f"{col:02d}".center(4)
    print(header)
    print()

    # Grid rows labels
    for row in range(height):
        node_line = f"{row:02d}  "
        edge_line = "    "

        for col in range(width):
            coords = (col, row)  # (x, y)

            if not g.node_at(coords):
                node_line += "   "
                edge_line += "   "
                continue

            # Node
            node_line += f"\033[91m{NODE_PATH}\033[0m" if coords in path_set else NODE_EMPTY

            # Right edge
            if col + 1 < width:
                w = g.weight[row][col][0] if hasattr(g.weight[row][col], '__getitem__') else 0
                right = (col + 1, row)
                if w > 0:
                    if is_path_edge(coords, right):
                        node_line += f"\033[91m{H_HEAVY*3}\033[0m"
                    else:
                        node_line += f"{cost_to_color(w)}{H_LIGHT*3}\033[0m"
                else:
                    node_line += "   "

            # Down edge (printed on next line)
            if row + 1 < height:
                w = g.weight[row][col][1]
                down = (col, row + 1)
                if w > 0:
                    if is_path_edge(coords, down):
                        edge_line += f"\033[91m{V_HEAVY}   \033[0m"
                    else:
                        edge_line += f"{cost_to_color(w)}{V_LIGHT}   \033[0m"
                else:
                    edge_line += "    "

        print(node_line)
        if row + 1 < height:
            print(edge_line)

    #Legend
    print("\nLegend:")
    print(f"  \033[38;5;41m{H_LIGHT*3} 1 ->\033[0m  Open terrain")
    print(f"  \033[38;5;63m{H_LIGHT*3} 2 ->\033[0m  Forest / hills")
    print(f"  \033[38;5;198m{H_LIGHT*3} 3 ->\033[0m Mountain / rough ")
    print(f"  \033[91m{NODE_PATH} {H_HEAVY*3} {V_HEAVY} ->\033[0m Path (highlighted in red) ")

if __name__ == '__main__':
    gr = create_grid_graph(10, 5)
    print(gr.weight[1][2])
    print_grid_graph(gr)
    for n in gr.neighbours((9,4)):
        print(n)

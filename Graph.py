import random
from typing import List, Tuple, Generator

# Terrain cost
COSTS = (1, 2, 3)
# ANSI colors
PATH = "93m"            # path color - bright yellow
# Unicode constants
H_LIGHT = "\u2500"      # ─ thin horizontal
H_HEAVY = "\u2501"      # ━ bold horizontal (path)
V_LIGHT = "\u2502"      # │ thin vertical
V_HEAVY = "\u2503"      # ┃ bold vertical (path)

NODE_EMPTY = "\u25cb"   # ○ open circle
NODE_PATH = "\u25cf"    # ● filled circle


class Graph:
    """
    An undirected and weighted 4-directional graph presented as rectangular grid.
    Each cell stores outgoing edge weights: [right_cost, down_cost].
    A weight of 0 means no edge between vertex a and b (blocked).    
    Internal representation: 1D list indexed by y * width + x
    External representation: 2D grid indexed by (x, y).
    """

    def __init__(self, width: int, height: int):
        """Initialize an empty graph with given dimensions."""
        self.width: int = width
        self.height: int = height
        self.size: int = width * height
        # Adjacency List
        self.weight: List[List[int]] = [
            [0, 0] for _ in range(self.size)
        ]

    def idx(self, x: int, y: int) -> int:
        """Convert 2D coordinates (x, y) to 1D index."""
        return y * self.width + x

    def node_at(self, coords: Tuple[int, int]) -> bool:
        """Check if coordinates are within grid bounds."""
        x, y = coords
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbours(
        self, coords: Tuple[int, int]
    ) -> Generator[tuple[tuple[int, int], int]]:
        """
        Yield valid adjacent vertices and the cost to move to them.
        Only yields neighbours with weight greater than 0.
        """
        x, y = coords
        w = self.weight[self.idx(x, y)]

        # Right edge
        if x + 1 < self.width and w[0] > 0:
            yield (x + 1, y), w[0]
        # Left edge - check the left vertex' right edge
        if x > 0 and self.weight[self.idx(x - 1, y)][0] > 0:
            yield (x - 1, y), self.weight[self.idx(x - 1, y)][0]
        # Down edge
        if y + 1 < self.height and w[1] > 0:
            yield (x, y + 1), w[1]
        # Up - check the upper vertex' down edge
        if y > 0 and self.weight[self.idx(x, y - 1)][1] > 0:
            yield (x, y - 1), self.weight[self.idx(x, y - 1)][1]


def create_grid_graph(
    width: int, height: int, seed: int | str = "Ucen2025", wall_probability: float = 0.10
) -> Graph:
    """
    Generate a graph with layout based seed parameter value used
    in random.Random and wall_probability parameter.    
    Edges are added with inverse probability to 
    wall_probability value.
    wall_probability = 0.1 -> 90 % to create an edge.
    Cost added randomly based on random.choice(seed)
    """
    rnd = random.Random(seed)
    g = Graph(width, height)

    for y in range(height):
        for x in range(width):
            cell_idx = g.idx(x, y)
            cell = g.weight[cell_idx]

            # Horizontal edge to the right
            if x + 1 < width and rnd.random() >= wall_probability:
                cell[0] = rnd.choice(COSTS)

            # Vertical edge downward
            if y + 1 < height and rnd.random() >= wall_probability:
                cell[1] = rnd.choice(COSTS)

    return g


def cost_to_color(cost: int) -> str:
    """Convert terrain cost to ANSI color."""
    if cost == 1:
        return "\033[38;5;41m"  # Dark gray - light terrain
    if cost == 2:
        return "\033[38;5;63m"  # Green - medium terrain
    if cost == 3:
        return "\033[38;5;198m"  # Purple - rough terrain
    return "\033[{PATH}"    # path colour

def print_grid_graph(
    g: Graph, path: list[tuple[tuple[int, int], float]] | None = None
) -> None:
    """
    Display the grid  to command-line terminal with colored terrain
    and highlighted path if found.    
    Uses Unicode box-drawing for edges, empty circles
    for not visited vertices.
    Path is shown in bright distinguish colour with bold lines
    for edges and full coloured circles for visited vertices.
    """
    path_set = set(coords for coords, _ in path) if path else set()

    def is_path_edge(a: tuple[int, int], b: tuple[int, int]) -> bool:
        """Membership testing - helper function."""
        return a in path_set and b in path_set

    # Column headers
    header = "  "
    for col in range(g.width):
        header += f"{col:02d}".center(4)
    print(header)
    print()

    # Build two rows at the time (vertices row and down edges row)
    for row in range(g.height):
        node_line = f"{row:02d}  " # Grid rows labels
        edge_line = "    "

        for col in range(g.width):
            coords = (col, row)

            cell = g.idx(col, row) # current vertex
            node_line += (
                f"\033[{PATH}{NODE_PATH}\033[0m" if coords in path_set else NODE_EMPTY # Node symbol
            )

            # Right edge
            if col + 1 < g.width:
                w = g.weight[cell][0]
                right = (col + 1, row)
                if w > 0:
                    if is_path_edge(coords, right):
                        node_line += f"\033[{PATH}{H_HEAVY * 3}\033[0m"
                    else:
                        node_line += f"{cost_to_color(w)}{H_LIGHT * 3}\033[0m"
                else:
                    node_line += "   "

            # Down edge (printed on next line)
            if row + 1 < g.height:
                w = g.weight[cell][1]
                down = (col, row + 1)
                if w > 0:
                    if is_path_edge(coords, down):
                        edge_line += f"\033[{PATH}{V_HEAVY}   \033[0m"
                    else:
                        edge_line += f"{cost_to_color(w)}{V_LIGHT}   \033[0m"
                else:
                    edge_line += "    "
    # Print both rows
        print(node_line)
        if row + 1 < g.height:
            print(edge_line)

    # Legend
    print("\nLegend:")
    print(f"  \033[38;5;41m{H_LIGHT * 3} 1 ->\033[0m  Open terrain")
    print(f"  \033[38;5;63m{H_LIGHT * 3} 2 ->\033[0m  Forest / hills")
    print(f"  \033[38;5;198m{H_LIGHT * 3} 3 ->\033[0m Mountain / rough ")
    print(f"  \033[{PATH}{NODE_PATH} {H_HEAVY * 3} {V_HEAVY} ->\033[0m Path")


if __name__ == "__main__":
    gr = create_grid_graph(10, 5)
    print_grid_graph(gr)
    for n in gr.neighbours((9, 4)):
        print(n)

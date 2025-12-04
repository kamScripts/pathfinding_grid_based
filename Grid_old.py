import random
from typing import Callable
class Graph:
    """Implementation of weighted, undirected Graph with private
    _Node and _Edge classes"""
#--------------------_Node structure for a graph----------------------------
    class _Node:
        """A node structure for undirected weighted graph."""
        __slots__='_coords', 'neighbours'
        def __init__(self, coords)->None:
            """Constructor should not be called directly, only by """
            self._coords = coords
            self.neighbours = {}
        def get_coords(self):
            """Return value attached to the node."""
            return self._coords
        def __repr__(self):
            return f"Node{self._coords}"
#-------------------- Graph Constructor----------------------------
    def __init__(self, width, height):
        """Create an empty weighted graph"""
        self._nodes = {}
        self._width = width
        self._height = height

    def node_at(self,coords):
        """Return a node at coordinates (row,column)."""
        return self._nodes.get(coords)

    def node_coords(self, node:_Node):
        """Return coordinates of a Node."""
        return node.get_coords()

    def add_node(self,coords:tuple[int,int])->_Node:
        """Create and return Node"""
        if coords in self._nodes:   #if node exists get it from _nodes
            return self._nodes[coords]
        node = self._Node(coords)
        self._nodes[coords] = node
        return node

    def  add_edge(self, origin:tuple[int, int], destination:tuple[int,int], weight=1.0)->None:
        origin_node = self.add_node(origin)
        d_node = self.add_node(destination)
     
        origin_node.neighbours[d_node] = weight
        d_node.neighbours[origin_node] = weight

    def remove_node(self, coords:tuple[int,int])->None:
        """Remove and return a node at coords (x,y)."""
        node= self._nodes.get(coords)
        #Remove all references
        for neighbour in list(node.neighbours.keys()):
            del neighbour.neighbours[node]
        #Remove a node from a Graph.
        del self._nodes[coords]

    def remove_edge(self, origin:tuple[int, int], destination:tuple[int, int])->None:
        """Remove edge between two nodes"""
        origin_node = self.node_at(origin)
        d_node = self.node_at(destination)
        if not origin_node or not d_node:
            raise ValueError('Node not found')
        if d_node in origin_node.neighbours:
            del origin_node.neighbours[d_node]
        if origin_node in d_node.neighbours:
            del d_node.neighbours[origin_node]

    def disconnect_node(self, coords: tuple[int, int]) -> None:
        """
        Disconnect a node from the graph by removing all its edges.
        The node remains in the graph but becomes isolated.
        """
        node = self.node_at(coords)
        if not node:
            raise ValueError(f"Node at {coords} not found")

        # Remove references from all neighbours
        for neighbour in list(node.neighbours.keys()):
            del neighbour.neighbours[node]

        # Clear this node's neighbour list
        node.neighbours.clear()

    def neighbours(self, coords: tuple[int, int]):
        """Yield (neighbor_coords, weight)"""
        node = self.node_at(coords)
        if node is None:
            return
        for neighbor_node, weight in node.neighbours.items():
            yield neighbor_node.get_coords(), weight

    def get_weight(self, origin, destination):
        origin_node = self.node_at(origin)
        d_node = self.node_at(destination)
        
        if origin_node and d_node:
            return origin_node.neighbours[d_node]
        return None
    def in_bounds(self, coords):
        """Check if coordinates are within graph bounds."""
        if not (isinstance(coords, tuple) and len(coords) == 2):
            return False
        x, y = coords
        return 0 <= x < self._width and 0 <= y < self._height
    def node_count(self):
        return len(self._nodes)

    def nodes(self):
        return iter(self._nodes.values())

    def is_connected(self, src, dst):
        """Quick check if two nodes have an edge."""
        return self.get_weight(src, dst) is not None

def create_grid_graph(
    width: int,
    height: int,
    terrain_cost_func: Callable,
    seed: int | str | None = None,
    wall_probability: float = 0.10   # 10% chance to remove edge
) -> Graph:
    """
    Creates a 4-connected grid graph
    """
    rnd = random.Random(seed)
    g = Graph(width, height)

    # Add all nodes first
    for row in range(height):
        for col in range(width):
            g.add_node((row, col))

    # Add edges
    for row in range(height):
        for col in range(width):
            # Right edge
            if col + 1 < width:
                if rnd.random() >= wall_probability:  # 90% chance to keep
                    cost = terrain_cost_func()
                    g.add_edge((row, col), (row, col + 1), cost)

            # Down edge
            if row + 1 < height:
                if rnd.random() >= wall_probability:
                    cost = terrain_cost_func()
                    g.add_edge((row, col), (row + 1, col), cost)

    return g

def terrain_cost() -> float:
    """
    Compute the movement cost between two adjacent nodes.
    """
    return random.choice([1,1.5,3])
def cost_to_color(cost):
    
    if cost == 1.0:
        return "\033[90m"       # Dark gray -light gravel path
    if cost == 1.5:
        return "\033[32m"       # Green-medium forest
    if cost == 3.0:
        return "\033[33m"       # Yellow-rough / rocky
    return "\033[91m"

def print_grid_graph(g: Graph, path: list[tuple[int, int]] | None = None):
    """
    Print CLI grid with colored edges and optional path overlay.
    Preserves spacing even when nodes/edges are removed.
    """
    path_set = set(path) if path else set()
    header = "  |"  # space for row numbers
    for col in range(g._width):
        header += f"{col:2d}   "   # two-digit columns
    print(header)
    print("  +","-"*(len(header)-6))
    for row in range(g._height):
        node_line = f"{row:2d}| "
        edge_line = "  | "
        for col in range(g._width):
            coords = (row, col)
            node = g.node_at(coords)

            # Node symbol (or placeholder if removed)
            if not node:
                node_line += "   "
                edge_line += "     "
                continue

            if coords in path_set:
                node_line += "\033[91m●\033[0m" # node symbol
            else:
                node_line += "\u25CB"

            # Horizontal edge
            right_coords = (row, col + 1)
            right_node = g.node_at(right_coords)
            if right_node and right_node in node.neighbours:
                cost = node.neighbours[right_node]
                color = cost_to_color(cost)
                if coords in path_set and right_coords in path_set:
                    node_line += "\033[91m----\033[0m"
                else:
                    node_line += f"{color}----\033[0m"
            else:
                node_line += "    "  # spacing for missing edge

            # Vertical edge
            down_coords = (row + 1, col)
            down_node = g.node_at(down_coords)
            if down_node and down_node in node.neighbours:
                cost = node.neighbours[down_node]
                color = cost_to_color(cost)
                if coords in path_set and down_coords in path_set:
                    edge_line += "\033[91m|    \033[0m"
                else:
                    edge_line += f"{color}|    \033[0m"
            else:
                edge_line += "     "  # spacing for missing edge

        print(node_line)
        if row + 1 < g._height:
            print(edge_line)
    print("  +","-"*(len(header)-6))
if __name__ == '__main__':
    gr = create_grid_graph(10, 10, terrain_cost)
        
    gr.disconnect_node((5,5))
    gr.remove_edge((0,0),(1,0))
    print_grid_graph(gr, [(9,9),(8,9),(7,9)])


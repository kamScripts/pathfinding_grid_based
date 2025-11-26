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
        # _coords in dunder methods is accessed directly to avoid overhead call to a getter
        def __hash__(self):
            """This method allows Node's coordinates (x,y) be a map or set key"""
            return hash(self._coords)
        def __eq__(self, other):
            return isinstance(other, Graph._Node) and self._coords == other._coords
        def __repr__(self):
            return f"Node{self._coords}"
#-------------------- Graph Constructor----------------------------
    def __init__(self, width, height):
        """Create an empty weighted graph"""
        self._nodes = {}
        self._width = width
        self._height = height
    def node_at(self,coords):
        """Return a node at coordinates (x,y)."""
        return self._nodes.get(coords)
    def node_coords(self, node:_Node):
        """Return coordinates of a Node."""
        return node.get_coords()
#-------------------- CREATE AND DE----------------------------
    def add_node(self,coords:tuple[int,int])->_Node:
        """Create and return Node"""
        if coords in self._nodes:   #if node exists get it from _nodes
            return self._nodes[coords]
        node = self._Node(coords)
        self._nodes[coords] = node
        return node
    def  add_edge(self, origin:tuple[int, int], destination:tuple[int,int], weight=1)->None:
        origin_node = self.add_node(origin)
        d_node = self.add_node(destination)
        
        origin_node.neighbours[d_node] = weight
        d_node.neighbours[origin_node] = weight
    def remove_node(self, coords:tuple[int,int])->_Node:
        """Remove and return a node at coords (x,y)."""
        node= self._nodes.get(coords)
        #Remove all references
        for neighbour in list(node.neighbours.keys()):
            del neighbour.neighbours[node]
        #Remove a node from a Graph.
        del self._nodes[coords]
        return node 
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
    def neighbours(self, coords):
        """Return an iteration of all valid endpoints and weights"""
        node = self.node_at(coords)
        if node:
            yield from node.neighbours.items()
    def get_weight(self, origin, destination):
        origin_node = self.node_at(origin)
        d_node = self.node_at(destination)
        
        if origin_node and d_node:
            return origin_node.neighbours[d_node]
        return None
    def in_bounds(self, coords):
        return 0<=coords[0]<self._width and 0<coords[1]<self._height
    def node_count(self):
        return len(self._nodes)
    def nodes(self):
        return iter(self._nodes.values())
    def clear(self):
        self._nodes.clear()

def create_grid_graph(width, height, terrain_cost_func):
    """
    Creates a 4-connected grid graph with proper undirected edges (no duplicates).
    """
    g = Graph(width, height)
    
    # Add all nodes
    for row in range(height):
        for col in range(width):
            g.add_node((row, col))
    
    # Add horizontal and vertical edges
    for row in range(height):
        for col in range(width):
            # Right neighbor
            if col + 1 < width:
                cost = terrain_cost_func(row, col, row, col + 1)
                g.add_edge((row, col), (row, col + 1), cost)
            
            # Down neighbor
            if row + 1 < height:
                cost = terrain_cost_func(row, col, row + 1, col)
                g.add_edge((row, col), (row + 1, col), cost)
    
    return g


def terrain_cost(
    row_from: int, col_from: int,
    row_to: int, col_to: int
) -> float:
    """
    Compute the movement cost between two adjacent grid cells.
"""
    if row_from == 0 and col_from <6:
        return 1.0
    elif (row_from + col_from) % 3 == 0:
        return 1.0   # flat terrain
    elif (row_from + col_from) % 3 == 1:
        return 1.5   # moderately rough terrain
    else:
        return 5.0   # very rough terrain



def print_grid_graph(g: Graph, terrain_func):
    """Print ASCII grid with terrain costs."""
    for row in range(g._height):
        line = []
        for col in range(g._width):
            cost = terrain_func(row, col, row, col)  # self-cost
            if cost == 1:
                line.append(".")   # flat terrain
            elif cost == 5:
                line.append("~")   # very rough terrain
            else:
                line.append("#")   # rough
        print("".join(line))


if __name__ == '__main__':
    gr = create_grid_graph(30, 10, terrain_cost)
    print_grid_graph(gr, terrain_cost)


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
    def add_node(self,coords:tuple[int,int])->_Node:
        """Create and return Node"""
        if coords in self._nodes:   #if node exists get it from _nodes
            return self._nodes[coords]
        node = self._Node(coords)
        self._nodes[coords] = node
        return node
    def  add_edge(self, origin:tuple[int, int], destination:tuple[int,int], weight=1)->None:
        o_node = self.add_node(origin)
        d_node = self.add_node(destination)
        
        o_node.neighbours[d_node] = weight
        d_node.neighbours[o_node] = weight
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
        o_node = self.node_at(origin)
        d_node = self.node_at(destination)
        
        if not o_node or not d_node:
            raise ValueError('Node not found')
        if d_node in o_node.neighbours:
            del o_node.neighbours[d_node]
        if o_node in d_node.neighbours:
            del d_node.neighbours[o_node]
    def neighbours(self, coords):
        """Return an iteration of all valid endpoints and weights"""
        node = self.node_at(coords)
        if node:
            yield from node.neighbours.items()
    def get_weight(self, origin, destination):
        o_node = self.node_at(origin)
        d_node = self.node_at(destination)
        
        if o_node and d_node:
            return o_node.neighbours[d_node]
        return None
    def in_bounds(self, coords):
        return 0<=coords[0]<self._width and 0<coords[1]<self._height
    def node_count(self):
        return len(self._nodes)
    def nodes(self):
        return iter(self._nodes.values())
    def clear(self):
        self._nodes.clear()
        
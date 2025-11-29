"""
First Structure to form grid-map, deprecated after implementing a Graph ADT."""
import random

class Grid:
    """Game-board for an algorithms presentation"""
    
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.data = {
            (r, c): {}
            for r in range(rows) for c in range(cols)
        }
    def add_edge(self,origin,destination,weight):
        self.data[origin][destination] = weight
        self.data[destination][origin] = weight
    

    def __repr__(self) -> str:
        """Representation of an object enabling grid reproduction."""
        return f"Grid(rows={self.rows}, cols={self.cols})"
    def __len__(self) -> int:
        """Return number of tiles"""
        return len(self.data)

  
if __name__ == '__main__':
    board=Grid(10,20)
    print(board.data.get((0,0)))
    board.move((0,0))
    print(board)
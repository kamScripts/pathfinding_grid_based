import random
class Grid:
    """Game-board for a algorithms presentation"""
    # Terrain type:  grass, water, wall
    TERRAIN = [',','~','#']

    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.data = {
            (r, c): {'cost': 1, 'terrain': '*'}
            for r in range(rows) for c in range(cols)
        }
        self.add_terrain()

    def __str__(self):
        return '\n'.join(
        ' '.join(str(self.data[(r, c)]['terrain']) for c in range(self.cols))
        for r in range(self.rows)
        )
    def __repr__(self) -> str:
        return f"Grid(rows={self.rows}, cols={self.cols})"
    
    def add_terrain(self, count: int = 30) -> None:
        """Randomly assigns terrain and cost to `count` tiles."""
        for _ in range(count):
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            terrain = random.choice(self.TERRAIN)
            cost = {
                'grass': 2,
                'water': 5,
                'wall': float('inf')  
            }
            self.data[(r, c)] = {'terrain': terrain, 'cost': cost}
board=Grid(10,10)
print((board))
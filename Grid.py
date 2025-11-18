import random

class Grid:
    """Game-board for an algorithms presentation"""

    TERRAIN = ['grass', 'water', 'wall']
    TERRAIN_COST = {
        'gravel': 1,
        'grass': 2,
        'water': 5,
        'wall': float('inf')  # Impassable
    }
    TERRAIN_SYMBOL = {
        'gravel': ':',
        'grass': ',',
        'water': '~',
        'wall': '#'
    }

    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.data = {
            (r, c): {'cost': self.TERRAIN_COST['gravel'], 'terrain': 'gravel', 'player': False}
            for r in range(rows) for c in range(cols)
        }
        self.add_terrain(count=50, seed=42)

    def __str__(self) -> str:
        """Readable representation of a grid."""
        return '\n'.join(
            ' '.join(self.TERRAIN_SYMBOL[self.data[(r, c)]['terrain']] for c in range(self.cols))
            for r in range(self.rows)
        )

    def __repr__(self) -> str:
        """Representation of an object enabling grid reproduction."""
        return f"Grid(rows={self.rows}, cols={self.cols})"

    def add_terrain(self, count: int = 30, seed: int | None = None) -> None:
        """Randomly assigns terrain and cost to `count` unique tiles.
        Seed parameter enables same map output"""
        if seed is not None:
            random.seed(seed)

        used = set()
        while len(used) < count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) in used:
                continue
            terrain = random.choice(self.TERRAIN)
            self.data[(r, c)] = {
                'terrain': terrain,
                'cost': self.TERRAIN_COST[terrain]
            }
            used.add((r, c))
    def move(self, coords:tuple[int,int], obj='x')->None:
        """Update position on a board."""
        
        
        
if __name__ == '__main__':
    board=Grid(20,20)
    print(board.TERRAIN_COST['wall'])
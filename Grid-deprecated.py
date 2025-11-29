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
            (r, c): {
                'cost': self.TERRAIN_COST['gravel'],
                'terrain': 'gravel',
                'occupied': False
            }
            for r in range(rows) for c in range(cols)
        }
        self.add_terrain(count=50)

    def __str__(self) -> str:
        # Column header
        header = '    ' + ' '.join(f'{c:2}' for c in range(self.cols)) + '\n'
        lines = [header]
    
        for r in range(self.rows):
            row = f'{r:2} | '   # Row header
            for c in range(self.cols):
                tile = self.data[(r, c)]
                symbol = 'X' if tile.get('occupied') else self.TERRAIN_SYMBOL[tile['terrain']]
                row += f'{symbol:2} '
            lines.append(row)
    
        return '\n'.join(lines)

    def __repr__(self) -> str:
        """Representation of an object enabling grid reproduction."""
        return f"Grid(rows={self.rows}, cols={self.cols})"
    def __len__(self) -> int:
        """Return number of tiles"""
        return len(self.data)

    def add_terrain(self, count: int = 50, seed: int | None = None) -> None:
        """Randomly assigns terrain and cost to `count` unique tiles.
        Seed parameter enables same map output"""
        if seed is not None:
            random.seed(seed)

        used = set()
        while len(used) < count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            # skip already replaced tiles
            if (r, c) in used:
                continue
            terrain = random.choice(self.TERRAIN)
            self.data[(r, c)] = {
                'terrain': terrain,
                'cost': self.TERRAIN_COST[terrain],
                'occupied': sel]f.data[(r, c)]['occupied']
            }
            used.add((r, c))
    def move(self, coords:tuple[int,int], obj='X')->None:
        """Update position on a board."""
        if self.data[coords]['terrain'] != 'wall':
            self.data[coords]['occupied'] = True
        
        
if __name__ == '__main__':
    board=Grid(10,20)
    print(board.data.get((0,0)))
    board.move((0,0))
    print(board)
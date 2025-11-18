class Grid:
    """Game-board for a algorithms presentation"""
    
    def __init__(self,rows, cols) -> None:
        self.rows=rows
        self.cols=cols
        self.data={
            (x,y):{'cost': 1, 'terrain': 0}
            for x in range(cols) for y in range(cols)}
    
    def __str__(self):
        output = ''
        for i in range(self.rows):
            for j in range(self.cols):
                output += f'{(self.data.get((i,j))['terrain'])} '
            output+='\n'
        return output

board=Grid(20,20)
print(board)
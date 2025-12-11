# grid/grid.py
class Grid:
    def __init__(self, rows=20, cols=30):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.traffic = [[1 for _ in range(cols)] for _ in range(rows)]
    
    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] != 1
    
    def get_neighbors(self, row, col):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self.is_valid(nr, nc):
                neighbors.append((nr, nc))
        return neighbors
    
    def get_cost(self, row, col):
        return self.traffic[row][col]

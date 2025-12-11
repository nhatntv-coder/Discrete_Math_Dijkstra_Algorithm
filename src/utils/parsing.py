# utils/parsing.py
from grid.grid import Grid

def prepare_grid(data):
    grid = Grid()
    
    for r, c in data.get('obstacles', []):
        grid.grid[r][c] = 1
    
    for r, c, cost in data.get('traffic', []):
        grid.traffic[r][c] = cost
    
    return grid

def get_points_list(data):
    start = tuple(data['start'])
    end = tuple(data['end'])
    stops = [tuple(s) for s in data.get('stops', [])]
    return [start] + stops + [end]

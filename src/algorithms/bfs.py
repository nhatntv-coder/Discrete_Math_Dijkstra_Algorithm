# algorithms/bfs.py
from collections import deque

def bfs_segment(grid, start, end):
    visited = set([start])
    queue = deque([(start, [start])])
    explored_order = []
    
    while queue:
        current, path = queue.popleft()
        explored_order.append(current)
        
        if current == end:
            total_cost = sum(grid.get_cost(r, c) for r, c in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

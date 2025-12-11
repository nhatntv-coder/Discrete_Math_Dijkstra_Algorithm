# algorithms/dfs.py
def dfs_segment(grid, start, end):
    visited = set()
    stack = [(start, [start])]
    explored_order = []
    
    while stack:
        current, path = stack.pop()
        
        if current in visited:
            continue
        
        visited.add(current)
        explored_order.append(current)
        
        if current == end:
            total_cost = sum(grid.get_cost(r, c) for r, c in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

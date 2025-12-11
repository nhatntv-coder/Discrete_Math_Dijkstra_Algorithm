# algorithms/multipoint.py
def run_multi_point_path(algo_func, grid, points):
    full_path = []
    full_explored = []
    total_cost = 0
    
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        
        path, explored, cost = algo_func(grid, start, end)
        
        if not path:
            return [], full_explored, float('inf')
        
        if i > 0:
            full_path.extend(path[1:])
        else:
            full_path.extend(path)
        
        full_explored.extend(explored)
        total_cost += cost
    
    return full_path, full_explored, total_cost

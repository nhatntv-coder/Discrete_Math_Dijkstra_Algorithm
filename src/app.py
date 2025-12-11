from flask import Flask, render_template, request, jsonify
import heapq
from collections import deque

app = Flask(__name__)

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

# --- Core Algorithms ---

def dijkstra_segment(grid, start, end):
    visited = set()
    distances = {start: 0}
    parent = {}
    pq = [(0, start)]
    explored_order = []
    
    while pq:
        dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        explored_order.append(current)
        
        if current == end:
            break
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                move_cost = grid.get_cost(neighbor[0], neighbor[1])
                new_dist = dist + move_cost
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
    
    path = []
    if end in parent or start == end: # Handle start==end case or path found
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()
    
    return path, explored_order, distances.get(end, float('inf'))

def bfs_segment(grid, start, end):
    visited = set([start])
    queue = deque([(start, [start])])
    explored_order = []
    
    while queue:
        current, path = queue.popleft()
        explored_order.append(current)
        
        if current == end:
            total_cost = sum(grid.get_cost(node[0], node[1]) for node in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

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
            total_cost = sum(grid.get_cost(node[0], node[1]) for node in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

# --- Multi-Point Orchestrator ---

def run_multi_point_path(algo_func, grid, points):
    """
    Chains the pathfinding between sequential points: Start -> Stop1 -> Stop2 -> End
    """
    full_path = []
    full_explored = []
    total_cost = 0
    
    # points is [start, stop1, stop2, ..., end]
    for i in range(len(points) - 1):
        segment_start = points[i]
        segment_end = points[i+1]
        
        path, explored, cost = algo_func(grid, segment_start, segment_end)
        
        if not path:
            return [], full_explored, float('inf') # Path broken
        
        # Avoid duplicating the join node (end of seg 1 is start of seg 2)
        if i > 0:
            full_path.extend(path[1:])
        else:
            full_path.extend(path)
            
        full_explored.extend(explored)
        total_cost += cost

    return full_path, full_explored, total_cost

@app.route('/')
def index():
    return render_template('index.html')

def prepare_grid(data):
    obstacles = data['obstacles']
    traffic_zones = data.get('traffic', [])
    
    grid = Grid()
    for obs in obstacles:
        grid.grid[obs[0]][obs[1]] = 1
    
    for traffic in traffic_zones:
        grid.traffic[traffic[0]][traffic[1]] = traffic[2]
    return grid

def get_points_list(data):
    start = tuple(data['start'])
    end = tuple(data['end'])
    stops = [tuple(s) for s in data.get('stops', [])]
    return [start] + stops + [end]

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    algorithm = data['algorithm']
    grid = prepare_grid(data)
    points = get_points_list(data)
    
    algos = {'dijkstra': dijkstra_segment, 'bfs': bfs_segment, 'dfs': dfs_segment}
    
    if algorithm in algos:
        path, explored, cost = run_multi_point_path(algos[algorithm], grid, points)
        return jsonify({
            'path': path,
            'explored': explored,
            'cost': cost,
            'nodes_explored': len(explored)
        })
    
    return jsonify({'error': 'Invalid algorithm'}), 400

@app.route('/run_all_simultaneous', methods=['POST'])
def run_all_simultaneous():
    data = request.json
    grid = prepare_grid(data)
    points = get_points_list(data)
    
    results = {}
    algos = {'dijkstra': dijkstra_segment, 'bfs': bfs_segment, 'dfs': dfs_segment}
    
    for name, func in algos.items():
        path, explored, cost = run_multi_point_path(func, grid, points)
        results[name] = {
            'path': path,
            'explored': explored,
            'cost': cost,
            'nodes_explored': len(explored),
            'path_length': len(path)
        }
    
    return jsonify(results)

@app.route('/compare_all', methods=['POST'])
def compare_all():
    # Reuse the same logic as run_all_simultaneous for comparison data
    return run_all_simultaneous()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
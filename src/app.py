from flask import Flask, render_template, request, jsonify
import heapq
from collections import deque
import math

app = Flask(__name__)

class Grid:
    def __init__(self, rows=20, cols=30):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.traffic = [[1 for _ in range(cols)] for _ in range(rows)]  # Traffic cost
    
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

def dijkstra(grid, start, end):
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
    if end in parent:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()
    
    return path, explored_order, distances.get(end, float('inf'))

def bfs(grid, start, end):
    visited = set([start])
    queue = deque([(start, [start])])
    explored_order = []
    
    while queue:
        current, path = queue.popleft()
        explored_order.append(current)
        
        if current == end:
            # Calculate actual cost for BFS path
            total_cost = sum(grid.get_cost(node[0], node[1]) for node in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

def dfs(grid, start, end):
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
            # Calculate actual cost for DFS path
            total_cost = sum(grid.get_cost(node[0], node[1]) for node in path[1:])
            return path, explored_order, total_cost
        
        for neighbor in grid.get_neighbors(*current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return [], explored_order, float('inf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    algorithm = data['algorithm']
    obstacles = data['obstacles']
    traffic_zones = data.get('traffic', [])
    start = tuple(data['start'])
    end = tuple(data['end'])
    
    grid = Grid()
    for obs in obstacles:
        grid.grid[obs[0]][obs[1]] = 1
    
    for traffic in traffic_zones:
        grid.traffic[traffic[0]][traffic[1]] = traffic[2]
    
    algorithms = {
        'dijkstra': dijkstra,
        'bfs': bfs,
        'dfs': dfs,
    }
    
    if algorithm in algorithms:
        path, explored, cost = algorithms[algorithm](grid, start, end)
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
    obstacles = data['obstacles']
    traffic_zones = data.get('traffic', [])
    start = tuple(data['start'])
    end = tuple(data['end'])
    
    grid = Grid()
    for obs in obstacles:
        grid.grid[obs[0]][obs[1]] = 1
    
    for traffic in traffic_zones:
        grid.traffic[traffic[0]][traffic[1]] = traffic[2]
    
    results = {}
    algorithms = {
        'dijkstra': dijkstra,
        'bfs': bfs,
        'dfs': dfs,
    }
    
    for name, algo in algorithms.items():
        path, explored, cost = algo(grid, start, end)
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
    data = request.json
    obstacles = data['obstacles']
    traffic_zones = data.get('traffic', [])
    start = tuple(data['start'])
    end = tuple(data['end'])
    
    grid = Grid()
    for obs in obstacles:
        grid.grid[obs[0]][obs[1]] = 1
    
    for traffic in traffic_zones:
        grid.traffic[traffic[0]][traffic[1]] = traffic[2]
    
    results = {}
    algorithms = {
        'Dijkstra': dijkstra,
        'BFS': bfs,
        'DFS': dfs,
    }
    
    for name, algo in algorithms.items():
        path, explored, cost = algo(grid, start, end)
        results[name] = {
            'path': path,
            'explored': explored,
            'cost': cost,
            'nodes_explored': len(explored),
            'path_length': len(path)
        }
    
    return jsonify(results)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Pathfinding Algorithm Visualizer")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("\nFeatures:")
    print("  • Visualize Dijkstra, BFS, DFS, and A* algorithms")
    print("  • Draw custom obstacles or generate random mazes")
    print("  • Compare all algorithms side-by-side")
    print("  • Interactive grid with drag-to-draw")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
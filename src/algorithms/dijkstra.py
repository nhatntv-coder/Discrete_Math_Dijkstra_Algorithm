# algorithms/dijkstra.py
import heapq

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
    
    # reconstruct path
    path = []
    if end in parent or start == end:
        node = end
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)
        path.reverse()
    
    return path, explored_order, distances.get(end, float('inf'))

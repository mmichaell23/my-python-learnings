import heapq

def dijkstra_optimized(graph, start):
    # Min-heap priority queue
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))

    # Dictionary for shortest distances
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Dictionary to track processed nodes
    processed = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If node is already processed, skip it
        if current_node in processed:
            continue
        processed.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Update only if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Example graph (Adjacency List Representation)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
shortest_paths = dijkstra_optimized(graph, start_node)
print("Shortest distances from node", start_node, ":", shortest_paths)
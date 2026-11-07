
import heapq
from collections import deque

graph = {
    "A": [("B", 1), ("C", 2)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 2), ("G", 10)],
    "D": [("G", 2)],
    "E": [("G", 1)],
    "F": [("G", 2)],
    "G": []
}


def ucs(start, goal):

    priority_queue = [(0, 0, start, [start])]
    best_cost = {start: 0}
    visit_order = []
    counter = 1

    while priority_queue:

        cost, _, node, path = heapq.heappop(priority_queue)

        if cost > best_cost.get(node, float("inf")):
            continue

        visit_order.append((node, cost))

        if node == goal:
            return path, cost, visit_order

        for neighbor, edge_cost in graph[node]:

            new_cost = cost + edge_cost

            if new_cost < best_cost.get(neighbor, float("inf")):

                best_cost[neighbor] = new_cost

                heapq.heappush(
                    priority_queue,
                    (new_cost, counter, neighbor, path + [neighbor])
                )

                counter += 1

    return None, None, visit_order


def bfs(start, goal):

    queue = deque([(start, [start])])
    visited = {start}

    while queue:

        node, path = queue.popleft()

        if node == goal:
            return path

        for neighbor, edge_cost in graph[node]:

            if neighbor not in visited:

                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


def calculate_cost(path):

    total = 0

    for i in range(len(path) - 1):

        for neighbor, edge_cost in graph[path[i]]:

            if neighbor == path[i + 1]:
                total += edge_cost
                break

    return total


ucs_path, ucs_cost, processing_order = ucs("A", "G")
bfs_path = bfs("A", "G")

print("UNIFORM COST SEARCH")
print("-------------------")

for step, item in enumerate(processing_order, 1):

    print(
        "Step:", step,
        "| Processed Node:", item[0],
        "| Path Cost:", item[1]
    )

print("\nUCS Result")
print("Path:", " -> ".join(ucs_path))
print("Total Cost:", ucs_cost)
print("Independently Calculated Cost:", calculate_cost(ucs_path))

print("\nBFS COMPARISON")
print("--------------")

print("BFS Path:", " -> ".join(bfs_path))
print("BFS Path Cost:", calculate_cost(bfs_path))
print("BFS Edges:", len(bfs_path) - 1)

print("\nUCS Edges:", len(ucs_path) - 1)
print("UCS Total Cost:", ucs_cost)

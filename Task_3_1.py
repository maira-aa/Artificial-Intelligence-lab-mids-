
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}


def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    visit_order = []

    while queue:
        node, path = queue.popleft()
        visit_order.append(node)

        if node == goal:
            return path, visit_order

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, visit_order


def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    visit_order = []

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        visit_order.append(node)

        if node == goal:
            return path, visit_order

        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None, visit_order


bfs_path, bfs_order = bfs("A", "G")
dfs_path, dfs_order = dfs("A", "G")

print("BREADTH-FIRST SEARCH")
print("--------------------")
print("Visit Order:", bfs_order)
print("Goal Path:", " -> ".join(bfs_path))
print("Path Depth:", len(bfs_path) - 1)

print("\nDEPTH-FIRST SEARCH")
print("------------------")
print("Visit Order:", dfs_order)
print("Goal Path:", " -> ".join(dfs_path))
print("Path Depth:", len(dfs_path) - 1)

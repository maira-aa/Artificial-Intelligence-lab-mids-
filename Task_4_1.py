
import heapq


graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

heuristic = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 2,
    "G": 0
}


def astar(graph, h, start, goal):
    queue = [(h[start], 0, start, [start])]
    best = {start: 0}
    processed = []
    expanded = 0

    while queue:
        f, g, node, path = heapq.heappop(queue)

        if g != best[node]:
            continue

        processed.append(node)

        if node == goal:
            return path, g, processed, expanded

        expanded += 1

        for nxt, cost in graph.get(node, []):
            new_cost = g + cost

            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                new_f = new_cost + h[nxt]
                heapq.heappush(
                    queue,
                    (new_f, new_cost, nxt, path + [nxt])
                )

    return None, float("inf"), processed, expanded


def path_cost(graph, path):
    total = 0

    if path is None:
        return total

    for i in range(len(path) - 1):
        for nxt, cost in graph[path[i]]:
            if nxt == path[i + 1]:
                total += cost
                break

    return total


def show_results(title, result, graph):
    path, cost, processed, expanded = result

    print("\n" + title)
    print("-" * 40)
    print("Returned Path:", " -> ".join(path) if path else "No path found")
    print("Returned Cost:", cost)
    print("Independently Calculated Cost:", path_cost(graph, path))
    print("Processed Nodes:", " -> ".join(processed))
    print("Expanded Nodes:", expanded)


print("TASK 1: MANUAL A* FRONTIER TRACE")
print("=" * 45)

frontier_steps = [
    ("After expanding S", [
        ("A", 1, 4, 5),
        ("B", 4, 4, 8)
    ]),
    ("After expanding A", [
        ("C", 3, 2, 5),
        ("B", 4, 4, 8)
    ]),
    ("After expanding C", [
        ("G", 6, 0, 6),
        ("B", 4, 4, 8)
    ])
]

for title, entries in frontier_steps:
    print("\n" + title)
    for node, g, h, f in entries:
        print("Node:", node, "| g:", g, "| h:", h, "| f:", f)


print("\n\nTASK 2: A* AND UCS COMPARISON")
print("=" * 45)

astar_result = astar(graph, heuristic, "S", "G")
show_results("A* Search", astar_result, graph)

zero_heuristic = {
    "S": 0,
    "A": 0,
    "B": 0,
    "C": 0,
    "G": 0
}

ucs_result = astar(graph, zero_heuristic, "S", "G")
show_results("UCS Search", ucs_result, graph)


print("\n\nTASK 3: OVERESTIMATED HEURISTIC")
print("=" * 45)

modified_heuristic = heuristic.copy()
modified_heuristic["C"] = 10

print("Original h(C):", heuristic["C"])
print("Modified h(C):", modified_heuristic["C"])
print("True Remaining Cost from C: 3")

modified_result = astar(
    graph,
    modified_heuristic,
    "S",
    "G"
)

show_results("A* With Overestimated Heuristic", modified_result, graph)


print("\n\nFINAL COMPARISON")
print("=" * 45)

print("Original A* Cost:", astar_result[1])
print("UCS Cost:", ucs_result[1])
print("Modified A* Cost:", modified_result[1])

print("Original A* Expansions:", astar_result[3])
print("UCS Expansions:", ucs_result[3])
print("Modified A* Expansions:", modified_result[3])

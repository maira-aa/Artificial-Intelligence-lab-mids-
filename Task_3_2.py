
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}


def dls(node, goal, limit, path):

    if node == goal:
        return "FOUND", path

    if limit == 0:
        if any(neighbor not in path for neighbor in graph[node]):
            return "CUTOFF", None
        return "FAILURE", None

    cutoff_found = False

    for neighbor in graph[node]:

        if neighbor not in path:

            status, result = dls(
                neighbor,
                goal,
                limit - 1,
                path + [neighbor]
            )

            if status == "FOUND":
                return status, result

            if status == "CUTOFF":
                cutoff_found = True

    if cutoff_found:
        return "CUTOFF", None

    return "FAILURE", None


print("DEPTH-LIMITED SEARCH")
print("--------------------")

for limit in range(1, 5):

    status, path = dls("A", "G", limit, ["A"])

    if path:
        path_result = " -> ".join(path)
    else:
        path_result = "Not found"

    print(
        "Limit:", limit,
        "| Status:", status,
        "| Path:", path_result
    )


print("\nITERATIVE DEEPENING DFS")
print("-----------------------")

for maximum_depth in range(1, 5):

    attempted_limits = []
    final_status = "FAILURE"
    final_path = None

    for limit in range(maximum_depth + 1):

        attempted_limits.append(limit)

        status, path = dls("A", "G", limit, ["A"])

        final_status = status

        if status == "FOUND":
            final_path = path
            break

    if final_path:
        path_result = " -> ".join(final_path)
    else:
        path_result = "Not found"

    print(
        "Maximum Depth:", maximum_depth,
        "| Limits:", attempted_limits,
        "| Status:", final_status,
        "| Path:", path_result
    )

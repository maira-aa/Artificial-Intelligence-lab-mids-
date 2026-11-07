
def minimax(scores, depth, index, is_max):
    if depth == 0:
        return scores[index], 1

    if is_max:
        left_value, left_count = minimax(scores, depth - 1, index * 2, False)
        right_value, right_count = minimax(scores, depth - 1, index * 2 + 1, False)
        return max(left_value, right_value), left_count + right_count

    left_value, left_count = minimax(scores, depth - 1, index * 2, True)
    right_value, right_count = minimax(scores, depth - 1, index * 2 + 1, True)
    return min(left_value, right_value), left_count + right_count


def alphabeta(scores, depth, index, is_max, alpha, beta):
    if depth == 0:
        return scores[index], 1

    count = 0

    if is_max:
        value = float("-inf")

        for i in range(2):
            child_value, child_count = alphabeta(
                scores, depth - 1, index * 2 + i,
                False, alpha, beta
            )

            count += child_count
            value = max(value, child_value)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value, count

    value = float("inf")

    for i in range(2):
        child_value, child_count = alphabeta(
            scores, depth - 1, index * 2 + i,
            True, alpha, beta
        )

        count += child_count
        value = min(value, child_value)
        beta = min(beta, value)

        if alpha >= beta:
            break

    return value, count


def run_test(scores, test_name):
    depth = 3

    minimax_value, minimax_count = minimax(
        scores, depth, 0, True
    )

    alpha_value, alpha_count = alphabeta(
        scores, depth, 0, True,
        float("-inf"), float("inf")
    )

    print("\n" + test_name)
    print("Leaf Values:", scores)
    print("Minimax Value:", minimax_value)
    print("Minimax Evaluated Leaves:", minimax_count)
    print("Alpha-Beta Value:", alpha_value)
    print("Alpha-Beta Evaluated Leaves:", alpha_count)


original_scores = [3, 5, 2, 9, 3, 5, 2, 9]
reordered_scores = [2, 9, 3, 5, 2, 9, 3, 5]

print("LAB 5: MINIMAX AND ALPHA-BETA PRUNING")

run_test(original_scores, "TEST 1: ORIGINAL BRANCH ORDER")

run_test(reordered_scores, "TEST 2: REORDERED BRANCHES")

print("\nFINAL COMPARISON")
print("Minimax always evaluates 8 leaves.")
print("Alpha-Beta evaluates fewer leaves when pruning is possible.")
print("Both algorithms return the same Minimax value.")

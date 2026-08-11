import heapq

INF = float('inf')


# ---------------------------------------------------
# Matrix Reduction
# ---------------------------------------------------

def reduce_matrix(mat):
    """
    Reduce the cost matrix and return:
    1. Reduced matrix
    2. Reduction cost
    """

    m = [row[:] for row in mat]
    n = len(m)
    cost = 0

    # Row reduction
    for i in range(n):

        row_min = min(m[i])

        if row_min != INF and row_min > 0:
            cost += row_min

            for j in range(n):
                if m[i][j] != INF:
                    m[i][j] -= row_min

    # Column reduction
    for j in range(n):

        col_min = min(m[i][j] for i in range(n))

        if col_min != INF and col_min > 0:
            cost += col_min

            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


# ---------------------------------------------------
# Travelling Salesman Problem - Branch and Bound
# ---------------------------------------------------

def tsp_branch_and_bound(cost, n):

    # Initial matrix reduction
    reduced_matrix, initial_cost = reduce_matrix(cost)

    # Heap elements:
    # (lower_bound, current_city, path, matrix)

    pq = []

    heapq.heappush(
        pq,
        (initial_cost, 0, [0], reduced_matrix)
    )

    best_cost = INF
    best_path = None

    while pq:

        # Get node with minimum lower bound
        bound, current, path, matrix = heapq.heappop(pq)

        # Pruning
        if bound >= best_cost:
            continue

        # If all cities are visited
        if len(path) == n:

            last_city = path[-1]

            # Check whether we can return to starting city
            if cost[last_city][0] != INF:

                total_cost = bound + cost[last_city][0]

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path + [0]

            continue

        # Try visiting every unvisited city
        for next_city in range(n):

            if next_city in path:
                continue

            if matrix[current][next_city] == INF:
                continue

            new_matrix = [row[:] for row in matrix]

            # Add the cost of travelling to next city
            new_bound = bound + matrix[current][next_city]

            # Set current row to INF
            for j in range(n):
                new_matrix[current][j] = INF

            # Set next city column to INF
            for i in range(n):
                new_matrix[i][next_city] = INF

            # Prevent returning to starting city too early
            new_matrix[next_city][0] = INF

            # Reduce the new matrix
            reduced_matrix, reduction_cost = reduce_matrix(new_matrix)

            new_bound += reduction_cost

            new_path = path + [next_city]

            # Push only promising nodes
            if new_bound < best_cost:

                heapq.heappush(
                    pq,
                    (
                        new_bound,
                        next_city,
                        new_path,
                        reduced_matrix
                    )
                )

    return best_path, best_cost


# ---------------------------------------------------
# Main Program
# ---------------------------------------------------

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

n = 5

cities = ['A', 'B', 'C', 'D', 'E']


# ---------------------------------------------------
# Display Cost Matrix
# ---------------------------------------------------

print("5-City TSP - Cost Matrix:\n")

print(f"{'':>5}", end="")

for city in cities:
    print(f"{city:>6}", end="")

print()

for i in range(n):

    print(f"{cities[i]:>5}", end="")

    for j in range(n):

        if cost[i][j] == INF:
            value = "INF"
        else:
            value = str(cost[i][j])

        print(f"{value:>6}", end="")

    print()


# ---------------------------------------------------
# Solve TSP
# ---------------------------------------------------

best_path, best_cost = tsp_branch_and_bound(cost, n)


# ---------------------------------------------------
# Display Result
# ---------------------------------------------------

print("\nOptimal Tour:")

print(
    " -> ".join(
        cities[i] for i in best_path
    )
)

print(f"Minimum Cost: {best_cost}")


# ---------------------------------------------------
# Path Verification
# ---------------------------------------------------

print("\nPath Verification:")

total = 0

for i in range(len(best_path) - 1):

    u = best_path[i]
    v = best_path[i + 1]

    edge_cost = cost[u][v]

    print(
        f"{cities[u]} -> {cities[v]} : cost = {edge_cost}"
    )

    total += edge_cost

print(f"\nTotal Cost = {total}")
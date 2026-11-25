import time
import random
import csv
import statistics
import matplotlib.pyplot as plt

from main import (
    merge_sort_parcels,
    knapsack_parcels,
    dijkstra,
    nearest_neighbor_tsp
)


def create_parcels(n):
    random.seed(42)

    parcels = []

    for i in range(n):
        parcels.append({
            "id": f"P{i}",
            "priority": random.randint(1, 5),
            "deadline": random.randint(1, 10),
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100)
        })

    return parcels


def create_graph(n):
    graph = {}

    nodes = [f"Location{i}" for i in range(n)]

    for i in range(n):
        graph[nodes[i]] = {}

        for j in range(n):
            if i != j:
                graph[nodes[i]][nodes[j]] = abs(i - j) + 1

    return graph


def measure_time(function, *args):
    times = []

    for _ in range(5):
        start = time.perf_counter()
        function(*args)
        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


def run_performance_test():

    sizes = [10, 20, 40, 80, 120]

    results = []

    print("\n===== PERFORMANCE TESTING =====")

    for n in sizes:

        parcels = create_parcels(n)
        graph = create_graph(n)

        sorting_time = measure_time(
            merge_sort_parcels, parcels
        )

        knapsack_time = measure_time(
            knapsack_parcels, parcels, 100
        )

        dijkstra_time = measure_time(
            dijkstra, graph, "Location0"
        )

        tsp_time = measure_time(
            nearest_neighbor_tsp, graph, "Location0"
        )

        results.append({
            "Input Size": n,
            "Merge Sort": sorting_time,
            "Knapsack DP": knapsack_time,
            "Dijkstra": dijkstra_time,
            "Nearest Neighbor TSP": tsp_time
        })

        print(f"\nInput Size: {n}")
        print(f"Merge Sort: {sorting_time:.8f} seconds")
        print(f"Knapsack DP: {knapsack_time:.8f} seconds")
        print(f"Dijkstra: {dijkstra_time:.8f} seconds")
        print(f"Nearest Neighbor TSP: {tsp_time:.8f} seconds")

    # Save results in CSV file
    with open("results/performance_results.csv",
              "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Input Size",
                "Merge Sort",
                "Knapsack DP",
                "Dijkstra",
                "Nearest Neighbor TSP"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    # Generate runtime comparison chart
    for algorithm in [
        "Merge Sort",
        "Knapsack DP",
        "Dijkstra",
        "Nearest Neighbor TSP"
    ]:

        plt.plot(
            [r["Input Size"] for r in results],
            [r[algorithm] for r in results],
            marker="o",
            label=algorithm
        )

    plt.xlabel("Input Size")
    plt.ylabel("Execution Time (Seconds)")
    plt.title("Algorithm Runtime Comparison")
    plt.legend()
    plt.grid(True)

    plt.savefig(
        "results/runtime_comparison.png"
    )

    plt.show()

    print("\nPerformance testing completed!")
    print("CSV saved in results folder.")
    print("Runtime graph saved in results folder.")


if __name__ == "__main__":
    run_performance_test()

"""
Mini-Courier Planner
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, and Nearest Neighbor TSP approximation.
Run: python main.py
"""
import json
import heapq
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def merge_sort_parcels(parcels):
    """Sort parcels by priority (high first), then deadline (early first)."""
    if len(parcels) <= 1:
        return parcels[:]
    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    return _merge(left, right)


def _parcel_key(parcel):
    # Lower tuple is better: negative priority gives descending priority.
    return (-parcel["priority"], parcel["deadline"], parcel["id"])


def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if _parcel_key(left[i]) <= _parcel_key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack_parcels(parcels, capacity):
    """
    0/1 Knapsack DP.
    Maximize total parcel value without exceeding vehicle capacity.
    Returns selected parcels, total weight, total value, and DP table.
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    value + dp[i - 1][cap - weight]
                )

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            cap -= parcel["weight"]

    selected.reverse()
    return {
        "selected": selected,
        "total_weight": sum(p["weight"] for p in selected),
        "total_value": sum(p["value"] for p in selected),
        "dp_table": dp,
    }


def dijkstra(graph, start):
    """Return shortest distances and predecessor map from start."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    if start not in graph:
        raise ValueError(f"Unknown start node: {start}")

    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance != distances[current]:
            continue

        for neighbor, weight in graph[current].items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, end):
    """Reconstruct a path using Dijkstra's predecessor map."""
    if end not in previous:
        return []
    path = []
    current = end
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]
    if path[-1] != start:
        return []
    return list(reversed(path))


def nearest_neighbor_tsp(graph, start):
    """
    Approximate a tour: repeatedly visit the nearest unvisited node,
    then return to the start when a return edge exists.
    """
    if start not in graph:
        raise ValueError(f"Unknown start node: {start}")
    unvisited = set(graph.keys())
    unvisited.remove(start)
    route = [start]
    total_distance = 0
    current = start

    while unvisited:
        candidates = [
            (distance, node)
            for node, distance in graph[current].items()
            if node in unvisited
        ]
        if not candidates:
            raise ValueError("Graph is not sufficiently connected for a full tour.")
        distance, next_node = min(candidates)
        total_distance += distance
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    if start in graph[current]:
        total_distance += graph[current][start]
        route.append(start)

    return route, total_distance


def load_data():
    with open(ROOT / "data" / "parcels.json", encoding="utf-8") as f:
        parcels = json.load(f)
    with open(ROOT / "data" / "graph.json", encoding="utf-8") as f:
        graph = json.load(f)
    return parcels, graph


def run_planner():
    parcels, graph = load_data()
    capacity = 15
    depot = "Depot"

    print("=" * 64)
    print("                 MINI-COURIER PLANNER")
    print("=" * 64)

    t0 = time.perf_counter()
    sorted_parcels = merge_sort_parcels(parcels)
    sort_time = time.perf_counter() - t0

    print("\n1. PARCEL PRIORITIZATION (Merge Sort)")
    print("ID   Priority   Deadline   Weight   Value")
    for p in sorted_parcels:
        print(f'{p["id"]:<4} {p["priority"]:<10} {p["deadline"]:<10} '
              f'{p["weight"]:<8} {p["value"]}')
    print(f"Sorting time: {sort_time:.8f} seconds")

    t0 = time.perf_counter()
    packing = knapsack_parcels(sorted_parcels, capacity)
    knapsack_time = time.perf_counter() - t0

    print("\n2. OPTIMAL PACKING (0/1 Knapsack DP)")
    print(f"Vehicle capacity: {capacity} kg")
    print("Selected parcels:", [p["id"] for p in packing["selected"]])
    print(f'Total weight: {packing["total_weight"]} kg')
    print(f'Total parcel value: {packing["total_value"]}')
    print(f"Knapsack time: {knapsack_time:.8f} seconds")

    print("\n3. SHORTEST PATHS (Dijkstra)")
    t0 = time.perf_counter()
    distances, previous = dijkstra(graph, depot)
    dijkstra_time = time.perf_counter() - t0
    for location in graph:
        if location != depot:
            path = reconstruct_path(previous, depot, location)
            print(f"{depot} -> {location}: {' -> '.join(path)} "
                  f"(distance: {distances[location]} km)")
    print(f"Dijkstra time: {dijkstra_time:.8f} seconds")

    print("\n4. DELIVERY TOUR (Nearest Neighbor TSP Approximation)")
    t0 = time.perf_counter()
    route, route_distance = nearest_neighbor_tsp(graph, depot)
    tsp_time = time.perf_counter() - t0
    print("Approximate route:", " -> ".join(route))
    print(f"Total tour distance: {route_distance} km")
    print(f"Nearest Neighbor time: {tsp_time:.8f} seconds")

    print("\n5. SUMMARY")
    print(f"Parcels selected: {len(packing['selected'])}/{len(parcels)}")
    print(f"Packing value: {packing['total_value']}")
    print(f"Delivery tour: {route_distance} km")
    print("All four algorithmic components executed successfully.")
    print("=" * 64)


if __name__ == "__main__":
    run_planner()

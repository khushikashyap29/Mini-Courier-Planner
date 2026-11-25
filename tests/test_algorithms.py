import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import merge_sort_parcels, knapsack_parcels, dijkstra, reconstruct_path, nearest_neighbor_tsp


class TestCourierPlanner(unittest.TestCase):
    def setUp(self):
        self.parcels = [
            {"id":"X","priority":2,"deadline":3,"weight":3,"value":40},
            {"id":"Y","priority":5,"deadline":2,"weight":4,"value":60},
            {"id":"Z","priority":5,"deadline":1,"weight":2,"value":30},
        ]

    def test_merge_sort_order(self):
        result = merge_sort_parcels(self.parcels)
        self.assertEqual([p["id"] for p in result], ["Z", "Y", "X"])

    def test_knapsack_capacity(self):
        result = knapsack_parcels(self.parcels, 5)
        self.assertLessEqual(result["total_weight"], 5)
        self.assertEqual(result["total_value"], 70)

    def test_dijkstra_and_path(self):
        graph = {"S":{"A":2,"B":5}, "A":{"S":2,"B":1}, "B":{"S":5,"A":1}}
        distances, previous = dijkstra(graph, "S")
        self.assertEqual(distances["B"], 3)
        self.assertEqual(reconstruct_path(previous, "S", "B"), ["S","A","B"])

    def test_nearest_neighbor(self):
        graph = {"S":{"A":2,"B":5}, "A":{"S":2,"B":1}, "B":{"S":5,"A":1}}
        route, distance = nearest_neighbor_tsp(graph, "S")
        self.assertEqual(route[0], "S")
        self.assertEqual(route[-1], "S")
        self.assertEqual(distance, 8)


if __name__ == "__main__":
    unittest.main()

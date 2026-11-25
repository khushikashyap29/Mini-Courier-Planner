# Mini-Courier Planner

**Developed By:** Khushi Kashyap  
**Roll Number:** 2501010082  
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Project:** Capstone Assignment – Mini-Courier Planner  
**Language:** Python 3  

---

## 1. Project Objective

The Mini-Courier Planner is a Python-based prototype that models a courier delivery service.

The system sorts parcels according to priority and deadline, selects valuable parcels within a limited vehicle capacity, calculates shortest paths from the depot, and generates an approximate delivery tour.

The project integrates sorting, dynamic programming, and graph algorithms into a single workflow.

## 2. Project Structure

```text
Mini-Courier-Planner/
│
├── main.py
├── performance.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── parcels.json
│   └── graph.json
│
├── tests/
│   └── test_algorithms.py
│
└── results/
    ├── screenshots/
    ├── performance_results.csv
    ├── sample_output.txt
    └── test_results.txt
```

Note: Python automatically generates `__pycache__` folders and compiled `.pyc` files. These are excluded from version control using `.gitignore`.

## 3. Requirements

- Python 3.9 or later
- No third-party Python package is required to run the main application.
- Matplotlib is required only for generating the performance comparison chart.

Install Matplotlib if needed:

```bash
pip install matplotlib
```

## 4. How to Run the Project

Follow these steps to execute the application:

1. Open the Mini-Courier-Planner folder in Visual Studio Code.
2. Open Terminal → New Terminal.
3. Check the Python installation:

```bash
python --version
```

4. Run the main application:

```bash
python main.py
```

If the `python` command does not work on Windows, try:

```bash
py main.py
```

## 5. Algorithms Used

### 5.1 Merge Sort

Merge Sort is used to arrange parcels according to their priority and deadline.

- Higher-priority parcels are placed first.
- If two parcels have the same priority, the parcel with the earlier deadline is placed first.

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

### 5.2 0/1 Knapsack using Dynamic Programming

The Knapsack algorithm selects a valuable combination of parcels without exceeding the vehicle's maximum weight capacity of 15 kg.

Each parcel can either be selected once or not selected.

**Time Complexity:** O(nW)  
**Space Complexity:** O(nW)

Here, `n` represents the number of parcels and `W` represents the vehicle capacity.

### 5.3 Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm calculates the shortest distances from the depot to all reachable delivery locations.

It uses an adjacency list and a min-priority queue. The road distances must be non-negative.

**Time Complexity:** O((V + E) log V)  
**Space Complexity:** O(V + E)

Here, `V` represents the number of vertices and `E` represents the number of edges.

### 5.4 Nearest Neighbor TSP Approximation

The Nearest Neighbor algorithm generates an approximate delivery tour.

It starts from the depot and repeatedly visits the nearest unvisited location. It returns to the depot when a return edge exists.

**Time Complexity:** O(V²)  
**Space Complexity:** O(V)

This is an approximation technique and does not guarantee the globally shortest tour.

## 6. Algorithm Workflow

The application follows these steps:

1. Load parcel and road network data from JSON files.
2. Sort parcels using Merge Sort.
3. Select parcels using 0/1 Knapsack DP with a 15 kg capacity.
4. Calculate shortest paths from the depot using Dijkstra's algorithm.
5. Generate an approximate delivery tour using Nearest Neighbor TSP.
6. Display selected parcels, shortest distances, delivery route, and execution timings.

## 7. Performance Testing

The project includes a performance testing script named `performance.py`.

Run the performance testing script using:

```bash
python performance.py
```

The script measures the execution time of all four algorithms:

- Merge Sort
- 0/1 Knapsack Dynamic Programming
- Dijkstra's Shortest Path
- Nearest Neighbor TSP Approximation

The experiment uses input sizes of 10, 20, 40, 80, and 120.

Each algorithm is executed five times for every input size, and the median execution time is recorded.

The generated files are:

- `results/performance_results.csv` – stores benchmark execution times.
- `results/screenshots/runtime_comparison.png` – displays the runtime comparison graph.

The execution times may vary depending on the computer and system conditions.

## 8. Running Automated Tests

The project includes automated unit tests to check the correctness of the implemented algorithms.

Run the tests using:

```bash
python -m unittest discover -s tests -v
```

All four automated unit tests passed during the recorded project testing.

## 9. Input Data

The project uses two JSON files:

### parcels.json

Contains parcel information:

- Parcel ID
- Priority
- Deadline
- Weight
- Value

### graph.json

Contains the weighted road network represented using an adjacency list.

Each location stores its connected neighboring locations and the corresponding road distances in kilometers.

The sample graph is undirected and stores reverse edges.

Users can modify these JSON files to experiment with different datasets.

## 10. Design Assumptions and Limitations

- Parcel priority is an integer from 1 to 5.
- A higher priority value represents greater importance.
- A smaller deadline value represents an earlier deadline.
- Knapsack maximizes total parcel value within the vehicle capacity.
- The Knapsack objective does not guarantee deadline feasibility.
- Road distances are non-negative.
- The road network is treated as an undirected graph.
- Nearest Neighbor is an approximation technique and may not produce the optimal TSP route.
- The sample road network is small and static.

## 11. Evidence Included

The `results/screenshots/` folder contains evidence of project execution and testing, including:

- Main program output screenshots
- Runtime comparison graph
- Performance-related screenshots

The `results/` folder also contains:

- `performance_results.csv` – benchmark data
- `sample_output.txt` – saved sample execution output
- `test_results.txt` – saved test results

## 12. Conclusion

The Mini-Courier Planner demonstrates the practical integration of four algorithmic techniques into a courier delivery planning system.

Merge Sort prioritizes parcels, Dynamic Programming selects a valuable parcel combination within vehicle capacity, Dijkstra calculates shortest paths, and Nearest Neighbor generates an approximate delivery tour.

The project also includes automated testing and performance analysis to evaluate the implementation.

## 13. Execution Commands – Quick Reference

**Run the main application:**

```bash
python main.py
```

**Run performance testing:**

```bash
python performance.py
```

**Run automated tests:**

```bash
python -m unittest discover -s tests -v
```

---

**Project Developed By: Khushi Kashyap**  
**Roll Number: 2501010082**
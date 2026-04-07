# Lab 4 - Dynamic Programming: Dijkstra and Floyd-Warshall

## Overview
This laboratory studies dynamic programming ideas through the implementation and empirical analysis of shortest-path algorithms: Dijkstra and Floyd-Warshall.

## Algorithms
- Dijkstra algorithm for single-source shortest paths
- Floyd-Warshall algorithm for all-pairs shortest paths

## Input Data Properties
- Graph types: sparse and dense
- Graph sizes: 20, 40, 60, 80, 100
- Weighted, connected, undirected graphs
- Positive edge weights only

## Metrics
- Execution time (milliseconds)
- Relaxations
- Updates
- Processed vertices / iterations
- Peak frontier size

## Usage
```bash
cd "d:\LAB 2\AA\lab 4"
python main.py
```

Quick mode:
```bash
python main.py --quick
```

Live interactive visualization:
```bash
python main.py --live
```

## Outputs
- `lab 4/lab4_results.json`
- `lab 4/lab4_results_quick.json`
- Graphs in `lab 4/graphs/`

## Bonus Visualization
The `--live` mode opens a real-time Matplotlib window that animates Dijkstra or Floyd--Warshall step by step on a small weighted graph.

## Report
The LaTeX report is available in `lab 4/report_lab4.tex` and follows the same style as the previous laboratory reports.

## Dependencies
```bash
pip install matplotlib
```

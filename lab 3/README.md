# Lab 3 — Empirical Analysis of DFS and BFS

## Overview 
Empirical comparison of **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** graph traversal algorithms across different graph types and sizes.

## Algorithms Implemented
| Algorithm | Strategy | Data Structure |
|---|---|---|
| DFS Iterative | Explore as deep as possible (iterative) | Explicit stack |
| DFS Recursive | Explore as deep as possible (recursive) | Call stack |
| BFS | Explore level-by-level | Queue (deque) |

## Input Data Properties
| Property | Values |
|---|---|
| Graph size (N) | 50, 100, 250, 500, 1000, 2000 |
| Graph type | Sparse (p=0.05), Medium (p=0.10), Dense (p=0.30), Tree, Grid |
| Starting vertex | Always vertex 0 |
| Seed | Fixed (42) for reproducibility |

## Metrics
- **Execution time** (ms) — wall-clock time averaged over 3 iterations
- **Nodes visited** — total nodes processed
- **Edges examined** — total neighbour-list accesses
- **Peak memory** — max stack / queue / recursion-depth during traversal

## Project Structure
```
lab 3/
├── graph.py               # Graph class + 5 graph generators
├── dfs_bfs.py             # DFS iterative, DFS recursive, BFS
├── performance_analyzer.py# Full sweep + averaging + JSON export
├── visualizer.py          # Matplotlib plots (saved to graphs/)
├── main.py                # Entry point (CLI)
├── README.md
└── graphs/                # Generated PNG files
```

## Usage
```bash
# Full analysis (all sizes, all graph types)
python main.py

# Quick test (small sizes, fast)
python main.py --quick

# Traversal demo on a tiny graph
python main.py --demo

# Re-generate plots from saved results
python main.py --load
```

## Dependencies
```bash
pip install matplotlib numpy
```

## Results
After running `python main.py`, all PNG charts are saved to `./graphs/` and the raw data is saved to `dfs_bfs_results.json`.

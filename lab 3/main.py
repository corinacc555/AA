"""
main.py - Entry point for Lab 3: DFS/BFS Empirical Analysis.

Usage
─────
  python main.py              # full analysis (all sizes, all graph types)
  python main.py --quick      # small sizes only — fast sanity check
  python main.py --load       # skip analysis, load saved results and re-plot
  python main.py --demo       # single small-graph traversal demo
"""

import argparse
import sys

from graph import Graph, GRAPH_TYPES, GraphGenerator
from dfs_bfs import ALGORITHMS, dfs_iterative, dfs_recursive, bfs
from performance_analyzer import PerformanceAnalyzer, DEFAULT_SIZES, RESULTS_FILE
from visualizer import Visualizer


# ─────────────────────────────────────────────────────────────────────────────
# Demo mode: walk through a tiny graph step by step
# ─────────────────────────────────────────────────────────────────────────────

def demo() -> None:
    print("=" * 60)
    print("TRAVERSAL DEMO — 12-node tree graph (always connected)")
    print("=" * 60)
    g = GraphGenerator.tree(12, seed=7)
    print(f"Graph: {g}")
    print("Adjacency list:")
    for v in g.get_vertices():
        print(f"  {v} → {g.get_neighbors(v)}")
    print()

    for name, fn in ALGORITHMS.items():
        m = fn(g, start=0)
        print(f"{name}")
        print(f"  Visited order : {m.visited_order}")
        print(f"  Nodes visited : {m.nodes_visited}")
        print(f"  Edges examined: {m.edges_examined}")
        print(f"  Peak memory   : {m.max_memory}")
        print(f"  Time          : {m.time_ms():.4f} ms")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# Quick test: small sizes for a fast verification run
# ─────────────────────────────────────────────────────────────────────────────

def quick_test() -> None:
    print("=" * 60)
    print("QUICK TEST — sizes [50, 100, 250]")
    print("=" * 60)
    analyzer = PerformanceAnalyzer()
    analyzer.run_full_analysis(sizes=[50, 100, 250], iterations=2)
    analyzer.print_summary()
    viz = Visualizer(analyzer.results)
    viz.plot_all()
    analyzer.save_results("dfs_bfs_results_quick.json")


# ─────────────────────────────────────────────────────────────────────────────
# Full analysis
# ─────────────────────────────────────────────────────────────────────────────

def full_analysis() -> None:
    print("=" * 60)
    print("FULL EMPIRICAL ANALYSIS")
    print(f"Sizes       : {DEFAULT_SIZES}")
    print(f"Graph types : {list(GRAPH_TYPES.keys())}")
    print(f"Algorithms  : {list(ALGORITHMS.keys())}")
    print(f"Iterations  : 3 per configuration")
    print("=" * 60)
    analyzer = PerformanceAnalyzer()
    analyzer.run_full_analysis(sizes=DEFAULT_SIZES, iterations=3)
    analyzer.print_summary()
    viz = Visualizer(analyzer.results)
    viz.plot_all()
    analyzer.save_results(RESULTS_FILE)
    print(f"\nDone. Results → {RESULTS_FILE}")
    print("Graphs      → ./graphs/")


# ─────────────────────────────────────────────────────────────────────────────
# Load + re-plot from saved JSON
# ─────────────────────────────────────────────────────────────────────────────

def load_and_plot() -> None:
    analyzer = PerformanceAnalyzer()
    analyzer.load_results(RESULTS_FILE)
    analyzer.print_summary()
    viz = Visualizer(analyzer.results)
    viz.plot_all()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lab 3 — DFS/BFS Empirical Analysis"
    )
    parser.add_argument("--quick", action="store_true",
                        help="Run a quick test with small graph sizes")
    parser.add_argument("--load",  action="store_true",
                        help="Load saved results and regenerate plots")
    parser.add_argument("--demo",  action="store_true",
                        help="Print a short traversal demo on a tiny graph")
    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.quick:
        quick_test()
    elif args.load:
        load_and_plot()
    else:
        full_analysis()


if __name__ == "__main__":
    main()

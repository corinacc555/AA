"""
performance_analyzer.py - Empirical analysis of DFS and BFS.

Runs each algorithm over a sweep of graph sizes and graph types, collects
averaged metrics over multiple iterations, and stores the results for later
visualisation and reporting.

Input data properties studied
──────────────────────────────
  • Graph size  : number of vertices N ∈ {50, 100, 250, 500, 1000, 2000}
  • Graph type  : sparse (p=0.05), medium (p=0.10), dense (p=0.30), tree, grid
  • Start vertex: always vertex 0 (deterministic, reproducible)

Metrics collected per run
─────────────────────────
  • Execution time   (milliseconds, 3-run average)
  • Nodes visited
  • Edges examined
  • Peak memory      (max stack / queue / recursion-depth)
"""

import json
import time
from typing import Dict, List, Any

from graph import Graph, GRAPH_TYPES
from dfs_bfs import ALGORITHMS, SearchMetrics


# Default experiment parameters
DEFAULT_SIZES      = [50, 100, 250, 500, 1000, 2000]
# Dense graphs become very heavy for large N; cap them here.
DENSE_MAX_SIZE     = 500
DEFAULT_ITERATIONS = 3
RESULTS_FILE       = "dfs_bfs_results.json"


class PerformanceAnalyzer:

    def __init__(self) -> None:
        # results[algo_name][graph_type] = list of dicts (one per size)
        self.results: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
            algo: {gtype: [] for gtype in GRAPH_TYPES}
            for algo in ALGORITHMS
        }

    # ──────────────────────────────────────────────────────────────────────
    # Core measurement
    # ──────────────────────────────────────────────────────────────────────

    def measure(
        self,
        algo_name: str,
        graph: Graph,
        iterations: int = DEFAULT_ITERATIONS,
    ) -> Dict[str, float]:
        """Run one algorithm on one graph `iterations` times and return averages."""
        algo_fn = ALGORITHMS[algo_name]
        times, nodes, edges, mems = [], [], [], []

        for seed_offset in range(iterations):
            # Each iteration uses the same graph but a fresh traversal
            m: SearchMetrics = algo_fn(graph, start=0)
            times.append(m.execution_time * 1000.0)   # ms
            nodes.append(m.nodes_visited)
            edges.append(m.edges_examined)
            mems.append(m.max_memory)

        return {
            "time_ms":        sum(times) / iterations,
            "nodes_visited":  sum(nodes) / iterations,
            "edges_examined": sum(edges) / iterations,
            "max_memory":     sum(mems)  / iterations,
        }

    # ──────────────────────────────────────────────────────────────────────
    # Full sweep: all algorithms × all graph types × all sizes
    # ──────────────────────────────────────────────────────────────────────

    def run_full_analysis(
        self,
        sizes: List[int] = DEFAULT_SIZES,
        iterations: int = DEFAULT_ITERATIONS,
    ) -> None:
        """Main entry-point: run every combination and populate self.results."""
        total = len(ALGORITHMS) * len(GRAPH_TYPES) * len(sizes)
        done = 0

        for gtype, gen_fn in GRAPH_TYPES.items():
            for n in sizes:
                # Skip very large dense graphs — O(n²) edges are too slow
                if gtype == "dense" and n > DENSE_MAX_SIZE:
                    done += len(ALGORITHMS)
                    continue

                graph = gen_fn(n)
                for algo_name in ALGORITHMS:
                    done += 1
                    print(
                        f"  [{done:3d}/{total}]  {algo_name:<17} | "
                        f"{gtype:<7} | n={n:5d}",
                        end=" ... ",
                        flush=True,
                    )
                    t_start = time.perf_counter()
                    stats = self.measure(algo_name, graph, iterations)
                    elapsed = time.perf_counter() - t_start
                    print(f"done ({elapsed*1000:.1f} ms total)")

                    self.results[algo_name][gtype].append(
                        {"n": n, **stats}
                    )

        print("\nAnalysis complete.")

    # ──────────────────────────────────────────────────────────────────────
    # Single-algorithm sweep (used by interactive mode in main.py)
    # ──────────────────────────────────────────────────────────────────────

    def analyze_single(
        self,
        algo_name: str,
        gtype: str,
        sizes: List[int] = DEFAULT_SIZES,
        iterations: int = DEFAULT_ITERATIONS,
    ) -> List[Dict[str, Any]]:
        gen_fn = GRAPH_TYPES[gtype]
        rows = []
        for n in sizes:
            if gtype == "dense" and n > DENSE_MAX_SIZE:
                continue
            graph = gen_fn(n)
            stats = self.measure(algo_name, graph, iterations)
            rows.append({"n": n, **stats})
        return rows

    # ──────────────────────────────────────────────────────────────────────
    # Save / load
    # ──────────────────────────────────────────────────────────────────────

    def save_results(self, filepath: str = RESULTS_FILE) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filepath}")

    def load_results(self, filepath: str = RESULTS_FILE) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self.results = json.load(f)
        print(f"Results loaded from {filepath}")

    # ──────────────────────────────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────────────────────────────

    def print_summary(self) -> None:
        print("\n" + "=" * 70)
        print("EMPIRICAL ANALYSIS SUMMARY — DFS vs BFS")
        print("=" * 70)

        for algo_name in ALGORITHMS:
            print(f"\n{'─'*70}")
            print(f"Algorithm: {algo_name}")
            print(f"{'─'*70}")
            print(f"{'Graph':<10} {'N':>6}  {'Time(ms)':>10}  "
                  f"{'Nodes':>8}  {'Edges':>10}  {'Mem':>8}")
            print(f"{'─'*70}")
            for gtype in GRAPH_TYPES:
                rows = self.results[algo_name][gtype]
                for row in rows:
                    print(
                        f"{gtype:<10} {row['n']:>6}  "
                        f"{row['time_ms']:>10.4f}  "
                        f"{row['nodes_visited']:>8.0f}  "
                        f"{row['edges_examined']:>10.0f}  "
                        f"{row['max_memory']:>8.0f}"
                    )
        print("=" * 70)

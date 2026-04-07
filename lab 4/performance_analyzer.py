"""
performance_analyzer.py - Empirical analysis for Dijkstra and Floyd–Warshall.
"""

from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from typing import Dict, List, Any

from weighted_graph import GRAPH_TYPES, WeightedGraphGenerator
from shortest_paths import dijkstra, floyd_warshall, PathMetrics


DEFAULT_SIZES = [20, 40, 60, 80, 100]
DEFAULT_ITERATIONS = 3
BASE_DIR = Path(__file__).resolve().parent
RESULTS_FILE = BASE_DIR / "lab4_results.json"


class PerformanceAnalyzer:
    def __init__(self) -> None:
        self.results: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
            "sparse": {"Dijkstra": [], "Floyd–Warshall": []},
            "dense": {"Dijkstra": [], "Floyd–Warshall": []},
        }

    def measure(self, algorithm: str, graph) -> PathMetrics:
        if algorithm == "Dijkstra":
            _, metrics = dijkstra(graph, 0)
            return metrics
        if algorithm == "Floyd–Warshall":
            _, metrics = floyd_warshall(graph)
            return metrics
        raise ValueError(f"Unknown algorithm: {algorithm}")

    def analyze_single(self, graph_type: str, sizes: List[int], iterations: int = DEFAULT_ITERATIONS) -> None:
        gen = GRAPH_TYPES[graph_type]
        for n in sizes:
            graph = gen(n, seed=42)
            for algorithm in ["Dijkstra", "Floyd–Warshall"]:
                times = []
                relaxations = []
                updates = []
                processed = []
                frontier = []
                for _ in range(iterations):
                    metrics = self.measure(algorithm, graph)
                    times.append(metrics.execution_time_ms)
                    relaxations.append(metrics.relaxations)
                    updates.append(metrics.updates)
                    processed.append(metrics.processed)
                    frontier.append(metrics.max_frontier)
                self.results[graph_type][algorithm].append({
                    "n": n,
                    "time_ms": sum(times) / iterations,
                    "relaxations": sum(relaxations) / iterations,
                    "updates": sum(updates) / iterations,
                    "processed": sum(processed) / iterations,
                    "max_frontier": sum(frontier) / iterations,
                })

    def run(self, sizes: List[int] = DEFAULT_SIZES, iterations: int = DEFAULT_ITERATIONS) -> None:
        print("=" * 72)
        print("LAB 4 - EMPIRICAL ANALYSIS OF DIJKSTRA AND FLOYD–WARSHALL")
        print("=" * 72)
        print(f"Sizes: {sizes}")
        print(f"Graph types: {list(GRAPH_TYPES.keys())}")
        print(f"Iterations: {iterations}")
        print("=" * 72)
        for graph_type in GRAPH_TYPES:
            print(f"\nAnalyzing {graph_type} graphs...")
            self.analyze_single(graph_type, sizes, iterations)

    def save_results(self, filepath: str = RESULTS_FILE) -> None:
        filepath = Path(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filepath}")

    def load_results(self, filepath: str = RESULTS_FILE) -> None:
        filepath = Path(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            self.results = json.load(f)

    def print_summary(self) -> None:
        print("\n" + "=" * 72)
        print("SUMMARY")
        print("=" * 72)
        for gtype, data in self.results.items():
            print(f"\nGraph type: {gtype}")
            for algo, rows in data.items():
                if not rows:
                    continue
                last = rows[-1]
                print(
                    f"  {algo:<15} N={last['n']:<4} time={last['time_ms']:.3f} ms "
                    f"relax={last['relaxations']:.0f} updates={last['updates']:.0f}"
                )

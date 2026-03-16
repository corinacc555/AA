"""
visualizer.py - Matplotlib plots for the DFS/BFS empirical analysis.

Generates and saves the following figures (all saved to ./graphs/):
  1. time_vs_size_<graph_type>.png    — Time vs N, one line per algorithm
  2. nodes_vs_size_<graph_type>.png   — Nodes visited vs N
  3. edges_vs_size_<graph_type>.png   — Edges examined vs N
  4. memory_vs_size_<graph_type>.png  — Peak memory vs N
  5. algo_comparison_n<N>.png         — Bar chart: all metrics at fixed N
  6. overview_heatmap.png             — Normalised time heat-map

Usage (from main.py):
    from visualizer import Visualizer
    viz = Visualizer(analyzer.results)
    viz.plot_all()
"""

import os
from typing import Dict, List, Any

import matplotlib
matplotlib.use("Agg")   # non-interactive backend; swap to TkAgg for windows
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from graph import GRAPH_TYPES
from dfs_bfs import ALGORITHMS

GRAPHS_DIR = "graphs"

# Colour and marker scheme — consistent across all plots
ALG_STYLE = {
    "DFS Iterative": {"color": "#2196F3", "marker": "o", "ls": "-"},
    "DFS Recursive": {"color": "#FF5722", "marker": "s", "ls": "--"},
    "BFS":           {"color": "#4CAF50", "marker": "^", "ls": "-."},
}

GTYPE_LABELS = {
    "sparse": "Sparse (p=0.05)",
    "medium": "Medium (p=0.10)",
    "dense":  "Dense  (p=0.30)",
    "tree":   "Tree",
    "grid":   "Grid",
}


class Visualizer:

    def __init__(self, results: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> None:
        self.results = results
        os.makedirs(GRAPHS_DIR, exist_ok=True)

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    def _extract(self, algo: str, gtype: str, key: str):
        rows = self.results[algo][gtype]
        xs = [r["n"] for r in rows]
        ys = [r[key] for r in rows]
        return xs, ys

    def _save(self, fig, filename: str) -> None:
        path = os.path.join(GRAPHS_DIR, filename)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved: {path}")

    # ──────────────────────────────────────────────────────────────────────
    # 1. Per-graph-type: metric vs. graph size
    # ──────────────────────────────────────────────────────────────────────

    def _plot_metric_vs_size(
        self,
        gtype: str,
        metric_key: str,
        ylabel: str,
        title_suffix: str,
        filename: str,
    ) -> None:
        fig, ax = plt.subplots(figsize=(8, 5))
        has_data = False
        for algo in ALGORITHMS:
            xs, ys = self._extract(algo, gtype, metric_key)
            if not xs:
                continue
            has_data = True
            st = ALG_STYLE[algo]
            ax.plot(
                xs, ys,
                label=algo,
                color=st["color"],
                marker=st["marker"],
                linestyle=st["ls"],
                linewidth=2,
                markersize=6,
            )
        if not has_data:
            plt.close(fig)
            return
        ax.set_xlabel("Graph Size (N — vertices)", fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(
            f"{title_suffix}\n{GTYPE_LABELS[gtype]}",
            fontsize=13,
            fontweight="bold",
        )
        ax.legend(fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.5)
        self._save(fig, filename)

    def plot_time_vs_size(self) -> None:
        for gtype in GRAPH_TYPES:
            self._plot_metric_vs_size(
                gtype, "time_ms",
                "Execution Time (ms)", "Execution Time vs. Graph Size",
                f"time_vs_size_{gtype}.png",
            )

    def plot_nodes_vs_size(self) -> None:
        for gtype in GRAPH_TYPES:
            self._plot_metric_vs_size(
                gtype, "nodes_visited",
                "Nodes Visited", "Nodes Visited vs. Graph Size",
                f"nodes_vs_size_{gtype}.png",
            )

    def plot_edges_vs_size(self) -> None:
        for gtype in GRAPH_TYPES:
            self._plot_metric_vs_size(
                gtype, "edges_examined",
                "Edges Examined", "Edges Examined vs. Graph Size",
                f"edges_vs_size_{gtype}.png",
            )

    def plot_memory_vs_size(self) -> None:
        for gtype in GRAPH_TYPES:
            self._plot_metric_vs_size(
                gtype, "max_memory",
                "Peak Memory (nodes)", "Peak Memory Usage vs. Graph Size",
                f"memory_vs_size_{gtype}.png",
            )

    # ──────────────────────────────────────────────────────────────────────
    # 2. Algorithm comparison bar chart at a fixed N
    # ──────────────────────────────────────────────────────────────────────

    def plot_algo_comparison(self, target_n: int = 500) -> None:
        """Grouped bar chart: for each graph type show all 3 algorithms side-by-side."""
        gtypes = list(GRAPH_TYPES.keys())
        algos  = list(ALGORITHMS.keys())
        n_groups = len(gtypes)
        n_bars   = len(algos)
        x = np.arange(n_groups)
        width = 0.25

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        metrics = [("time_ms", "Execution Time (ms)"),
                   ("max_memory", "Peak Memory (nodes)")]

        for ax_idx, (metric_key, ylabel) in enumerate(metrics):
            ax = axes[ax_idx]
            for i, algo in enumerate(algos):
                values = []
                for gtype in gtypes:
                    rows = self.results[algo][gtype]
                    # find the row closest to target_n
                    row = min(rows, key=lambda r: abs(r["n"] - target_n), default=None)
                    values.append(row[metric_key] if row else 0)
                st = ALG_STYLE[algo]
                offset = (i - 1) * width
                ax.bar(
                    x + offset, values, width,
                    label=algo,
                    color=st["color"],
                    edgecolor="white",
                    alpha=0.85,
                )
            ax.set_xticks(x)
            ax.set_xticklabels([GTYPE_LABELS[g] for g in gtypes], rotation=15, ha="right")
            ax.set_ylabel(ylabel, fontsize=11)
            ax.set_title(f"{ylabel}\n(N ≈ {target_n})", fontsize=12, fontweight="bold")
            ax.legend(fontsize=10)
            ax.grid(True, axis="y", linestyle="--", alpha=0.5)

        fig.suptitle("DFS vs BFS — Algorithm Comparison by Graph Type", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        self._save(fig, f"algo_comparison_n{target_n}.png")

    # ──────────────────────────────────────────────────────────────────────
    # 3. Heat-map: normalised execution time
    # ──────────────────────────────────────────────────────────────────────

    def plot_heatmap(self, target_n: int = 500) -> None:
        """Heat-map where rows=algorithms, cols=graph types, value=time (ms)."""
        algos  = list(ALGORITHMS.keys())
        gtypes = list(GRAPH_TYPES.keys())
        data   = np.zeros((len(algos), len(gtypes)))

        for i, algo in enumerate(algos):
            for j, gtype in enumerate(gtypes):
                rows = self.results[algo][gtype]
                row  = min(rows, key=lambda r: abs(r["n"] - target_n), default=None)
                data[i, j] = row["time_ms"] if row else 0.0

        fig, ax = plt.subplots(figsize=(9, 4))
        im = ax.imshow(data, cmap="YlOrRd", aspect="auto")
        plt.colorbar(im, ax=ax, label="Time (ms)")

        ax.set_xticks(range(len(gtypes)))
        ax.set_yticks(range(len(algos)))
        ax.set_xticklabels([GTYPE_LABELS[g] for g in gtypes], fontsize=11)
        ax.set_yticklabels(algos, fontsize=11)

        # Annotate cells
        for i in range(len(algos)):
            for j in range(len(gtypes)):
                ax.text(j, i, f"{data[i,j]:.3f}", ha="center", va="center",
                        fontsize=9, color="black" if data[i,j] < data.max()*0.7 else "white")

        ax.set_title(f"Execution Time Heat-Map (N ≈ {target_n})", fontsize=13, fontweight="bold")
        fig.tight_layout()
        self._save(fig, "overview_heatmap.png")

    # ──────────────────────────────────────────────────────────────────────
    # 4. All-metrics overview (2×2 for a single graph type)
    # ──────────────────────────────────────────────────────────────────────

    def plot_overview(self, gtype: str = "medium") -> None:
        """2×2 grid: time, nodes, edges, memory — for one graph type."""
        metrics = [
            ("time_ms",        "Time (ms)"),
            ("nodes_visited",  "Nodes Visited"),
            ("edges_examined", "Edges Examined"),
            ("max_memory",     "Peak Memory"),
        ]
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axes_flat = axes.flatten()

        for idx, (key, label) in enumerate(metrics):
            ax = axes_flat[idx]
            for algo in ALGORITHMS:
                xs, ys = self._extract(algo, gtype, key)
                if not xs:
                    continue
                st = ALG_STYLE[algo]
                ax.plot(xs, ys, label=algo, color=st["color"],
                        marker=st["marker"], linestyle=st["ls"],
                        linewidth=2, markersize=5)
            ax.set_xlabel("N (vertices)", fontsize=10)
            ax.set_ylabel(label, fontsize=10)
            ax.set_title(label, fontsize=11, fontweight="bold")
            ax.legend(fontsize=9)
            ax.grid(True, linestyle="--", alpha=0.4)

        fig.suptitle(
            f"DFS vs BFS — All Metrics Overview ({GTYPE_LABELS[gtype]})",
            fontsize=14, fontweight="bold",
        )
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        self._save(fig, f"overview_{gtype}.png")

    # ──────────────────────────────────────────────────────────────────────
    # Master call
    # ──────────────────────────────────────────────────────────────────────

    def plot_all(self) -> None:
        print("\nGenerating plots ...")
        self.plot_time_vs_size()
        self.plot_nodes_vs_size()
        self.plot_edges_vs_size()
        self.plot_memory_vs_size()
        self.plot_algo_comparison(target_n=500)
        self.plot_heatmap(target_n=500)
        for gtype in GRAPH_TYPES:
            self.plot_overview(gtype)
        print("All plots saved to ./graphs/")

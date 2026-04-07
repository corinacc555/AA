"""
visualizer.py - Graphical presentation of Lab 4 results.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
GRAPH_DIR = BASE_DIR / "graphs"

STYLE = {
    "Dijkstra": {"color": "#1976D2", "marker": "o"},
    "Floyd–Warshall": {"color": "#D32F2F", "marker": "s"},
}


class Visualizer:
    def __init__(self, results: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> None:
        self.results = results
        GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    def _save(self, fig, filename: str) -> None:
        path = GRAPH_DIR / filename
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved: {path}")

    def _plot_metric(self, graph_type: str, metric: str, ylabel: str, filename: str) -> None:
        fig, ax = plt.subplots(figsize=(9, 5))
        for algo, rows in self.results[graph_type].items():
            xs = [r["n"] for r in rows]
            ys = [r[metric] for r in rows]
            st = STYLE[algo]
            ax.plot(xs, ys, label=algo, color=st["color"], marker=st["marker"], linewidth=2)
        ax.set_title(f"{metric.replace('_', ' ').title()} - {graph_type.title()} graphs", fontweight="bold")
        ax.set_xlabel("Number of nodes (N)")
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()
        self._save(fig, filename)

    def plot_all(self) -> None:
        for graph_type in self.results:
            self._plot_metric(graph_type, "time_ms", "Execution time (ms)", f"time_{graph_type}.png")
            self._plot_metric(graph_type, "relaxations", "Relaxations", f"relaxations_{graph_type}.png")
            self._plot_metric(graph_type, "updates", "Updates", f"updates_{graph_type}.png")

            fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
            metrics = [("time_ms", "Time (ms)"), ("relaxations", "Relaxations"), ("updates", "Updates")]
            for ax, (metric, ylabel) in zip(axes, metrics):
                for algo, rows in self.results[graph_type].items():
                    xs = [r["n"] for r in rows]
                    ys = [r[metric] for r in rows]
                    st = STYLE[algo]
                    ax.plot(xs, ys, label=algo, color=st["color"], marker=st["marker"], linewidth=2)
                ax.set_xlabel("N")
                ax.set_ylabel(ylabel)
                ax.grid(True, linestyle="--", alpha=0.4)
                ax.legend(fontsize=8)
            fig.suptitle(f"Lab 4 Metrics Overview - {graph_type.title()} graphs", fontweight="bold")
            fig.tight_layout(rect=[0, 0, 1, 0.95])
            self._save(fig, f"overview_{graph_type}.png")

        # Combined comparison at the largest N in the dataset
        last_n = max(rows[-1]["n"] for rows in next(iter(self.results.values())).values() if rows)
        fig, ax = plt.subplots(figsize=(8, 5))
        labels = []
        values = []
        for graph_type in self.results:
            for algo in self.results[graph_type]:
                row = next((r for r in self.results[graph_type][algo] if r["n"] == last_n), None)
                if row:
                    labels.append(f"{graph_type[:1].upper()}-{algo[:1]}")
                    values.append(row["time_ms"])
        ax.bar(labels, values, color="#607D8B")
        ax.set_title(f"Execution Time at N={last_n}", fontweight="bold")
        ax.set_ylabel("Time (ms)")
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)
        self._save(fig, f"comparison_n{last_n}.png")

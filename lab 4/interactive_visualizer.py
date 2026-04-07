"""
interactive_visualizer.py - Real-time interactive visualization for Lab 4.

This module provides a menu-driven live demo for Dijkstra and Floyd--Warshall.
It shows the algorithms step by step using Matplotlib animations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from heapq import heappop, heappush
from collections import deque
from typing import Dict, Generator, List, Optional, Set, Tuple

import matplotlib
try:
    matplotlib.use("TkAgg")
except Exception:
    pass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from weighted_graph import GRAPH_TYPES, WeightedGraphGenerator, WeightedGraph


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def circular_layout(graph: WeightedGraph) -> Dict[int, Tuple[float, float]]:
    vertices = graph.get_vertices()
    count = len(vertices)
    if count == 0:
        return {}
    positions = {}
    for index, vertex in enumerate(vertices):
        angle = 2.0 * math.pi * index / count
        positions[vertex] = (math.cos(angle), math.sin(angle))
    return positions


# ---------------------------------------------------------------------------
# Dijkstra state generator
# ---------------------------------------------------------------------------

def dijkstra_states(graph: WeightedGraph, source: int = 0) -> Generator[dict, None, None]:
    n = graph.num_vertices
    dist = [math.inf] * n
    dist[source] = 0.0
    visited: Set[int] = set()
    heap: List[Tuple[float, int]] = [(0.0, source)]

    yield {
        "step": 0,
        "current": None,
        "visited": set(),
        "frontier": {source},
        "dist": dist.copy(),
        "message": "Initialized source node.",
    }

    step = 0
    while heap:
        step += 1
        current_distance, node = heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        yield {
            "step": step,
            "current": node,
            "visited": set(visited),
            "frontier": {v for _, v in heap},
            "dist": dist.copy(),
            "message": f"Processing node {node} with distance {current_distance:.2f}.",
        }

        for neighbour, weight in graph.get_neighbors(node):
            candidate = current_distance + weight
            if candidate < dist[neighbour]:
                dist[neighbour] = candidate
                heappush(heap, (candidate, neighbour))
                step += 1
                yield {
                    "step": step,
                    "current": node,
                    "visited": set(visited),
                    "frontier": {v for _, v in heap},
                    "dist": dist.copy(),
                    "message": (
                        f"Relaxed edge {node} -> {neighbour} with weight {weight}; "
                        f"new distance {candidate:.2f}."
                    ),
                }

    yield {
        "step": step + 1,
        "current": None,
        "visited": set(visited),
        "frontier": set(),
        "dist": dist.copy(),
        "message": "Dijkstra completed.",
    }


# ---------------------------------------------------------------------------
# Floyd--Warshall state generator
# ---------------------------------------------------------------------------

def floyd_states(graph: WeightedGraph) -> Generator[dict, None, None]:
    n = graph.num_vertices
    dist = np.full((n, n), np.inf)
    np.fill_diagonal(dist, 0.0)

    for u in graph.get_vertices():
        for v, w in graph.get_neighbors(u):
            if w < dist[u, v]:
                dist[u, v] = float(w)

    yield {
        "step": 0,
        "k": None,
        "dist": dist.copy(),
        "message": "Initialized distance matrix.",
    }

    step = 0
    for k in range(n):
        step += 1
        updated = False
        for i in range(n):
            dik = dist[i, k]
            if math.isinf(dik):
                continue
            for j in range(n):
                candidate = dik + dist[k, j]
                if candidate < dist[i, j]:
                    dist[i, j] = candidate
                    updated = True
                    step += 1
                    yield {
                        "step": step,
                        "k": k,
                        "dist": dist.copy(),
                        "message": f"Updated dist[{i}][{j}] via k={k}.",
                    }
        yield {
            "step": step,
            "k": k,
            "dist": dist.copy(),
            "message": f"Completed iteration k={k}." if updated else f"No updates at k={k}.",
        }

    yield {
        "step": step + 1,
        "k": None,
        "dist": dist.copy(),
        "message": "Floyd--Warshall completed.",
    }


# ---------------------------------------------------------------------------
# Animator
# ---------------------------------------------------------------------------

@dataclass
class LiveConfig:
    algorithm: str
    graph_type: str
    size: int
    seed: int = 42
    interval_ms: int = 400


class LiveVisualizer:
    def __init__(self, config: LiveConfig) -> None:
        self.config = config
        self.graph = WeightedGraphGenerator.generate(config.graph_type, config.size, seed=config.seed)
        self.positions = circular_layout(self.graph)
        self.anim = None

        self.fig = None
        self.ax_main = None
        self.ax_text = None
        self.edge_lines = []
        self.node_scatter = None
        self.node_labels = {}
        self.dist_texts = {}

    def _draw_graph_static(self) -> None:
        self.fig, (self.ax_main, self.ax_text) = plt.subplots(
            1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": [3, 1]}
        )
        self.ax_main.set_title(
            f"{self.config.algorithm} - {self.config.graph_type.title()} graph (N={self.config.size})",
            fontsize=13,
            fontweight="bold",
        )
        self.ax_main.axis("off")
        self.ax_text.axis("off")

        # Draw edges
        drawn = set()
        for u in self.graph.get_vertices():
            x1, y1 = self.positions[u]
            for v, w in self.graph.get_neighbors(u):
                key = tuple(sorted((u, v)))
                if key in drawn:
                    continue
                drawn.add(key)
                x2, y2 = self.positions[v]
                self.ax_main.plot([x1, x2], [y1, y2], color="#cccccc", linewidth=1, zorder=1)
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax_main.text(mid_x, mid_y, str(w), fontsize=8, color="#555555")

        # Draw nodes
        xs = [self.positions[v][0] for v in self.graph.get_vertices()]
        ys = [self.positions[v][1] for v in self.graph.get_vertices()]
        self.node_scatter = self.ax_main.scatter(xs, ys, s=300, c="#9e9e9e", zorder=3)
        for v in self.graph.get_vertices():
            x, y = self.positions[v]
            self.node_labels[v] = self.ax_main.text(
                x, y, str(v), ha="center", va="center", color="white", fontsize=9, zorder=4
            )

        self.ax_main.text(0.01, 0.02, "gray=unvisited | blue=frontier | orange=current | green=visited",
                          transform=self.ax_main.transAxes, fontsize=9)

    def _draw_text_panel(self, state: dict) -> None:
        self.ax_text.clear()
        self.ax_text.axis("off")
        lines = [
            f"Step: {state.get('step', 0)}",
            f"Current: {state.get('current', '-')}",
            f"Message: {state.get('message', '')}",
        ]
        if "k" in state and state.get("k") is not None:
            lines.insert(1, f"k: {state['k']}")
        if "dist" in state:
            dist = state["dist"]
            show = min(len(dist), 12)
            dist_lines = ["Distances:"]
            for idx in range(show):
                value = dist[idx]
                value_text = "∞" if math.isinf(value) else f"{value:.1f}"
                dist_lines.append(f"d[{idx}] = {value_text}")
            if len(dist) > show:
                dist_lines.append("...")
            lines.extend([""] + dist_lines)
        self.ax_text.text(0.02, 0.98, "\n".join(lines), va="top", fontsize=10)

    def _apply_dijkstra_colors(self, state: dict) -> None:
        visited = state.get("visited", set())
        frontier = state.get("frontier", set())
        current = state.get("current", None)
        colors = []
        for vertex in self.graph.get_vertices():
            if vertex == current:
                colors.append("#ff9800")
            elif vertex in frontier:
                colors.append("#1976d2")
            elif vertex in visited:
                colors.append("#4caf50")
            else:
                colors.append("#9e9e9e")
        self.node_scatter.set_color(colors)

    def _update_floyd_matrix(self, dist: np.ndarray) -> None:
        if not hasattr(self, "matrix_ax"):
            self.matrix_ax = self.ax_main.inset_axes([0.78, 0.05, 0.2, 0.35])
            self.matrix_img = self.matrix_ax.imshow(dist, cmap="viridis")
            self.matrix_ax.set_title("Distance matrix", fontsize=8)
            self.matrix_ax.tick_params(labelsize=6)
            self.fig.colorbar(self.matrix_img, ax=self.matrix_ax, fraction=0.046, pad=0.04)
        else:
            display = np.where(np.isinf(dist), np.nan, dist)
            self.matrix_img.set_data(display)
            self.matrix_img.set_clim(np.nanmin(display), np.nanmax(display))

    def animate(self) -> None:
        self._draw_graph_static()
        algorithm = self.config.algorithm
        if algorithm == "Dijkstra":
            states = dijkstra_states(self.graph, source=0)

            def update(state: dict):
                self._apply_dijkstra_colors(state)
                self._draw_text_panel(state)
                return self.node_scatter,

        elif algorithm == "Floyd--Warshall":
            states = floyd_states(self.graph)

            def update(state: dict):
                self._update_floyd_matrix(state["dist"])
                self._draw_text_panel(state)
                return self.node_scatter,

        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        self.anim = animation.FuncAnimation(
            self.fig,
            update,
            frames=states,
            interval=self.config.interval_ms,
            repeat=False,
            cache_frame_data=False,
        )
        plt.tight_layout()
        plt.show()


# ---------------------------------------------------------------------------
# User menu
# ---------------------------------------------------------------------------

def _choose(prompt: str, options: List[str], default: int = 0) -> str:
    while True:
        print(f"\n{prompt}")
        for index, option in enumerate(options, start=1):
            marker = " (default)" if index - 1 == default else ""
            print(f"  {index}. {option}{marker}")
        raw = input("Select option: ").strip()
        if not raw:
            return options[default]
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Invalid selection. Try again.")


def _ask_int(prompt: str, default: int, min_value: int, max_value: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit():
            value = int(raw)
            if min_value <= value <= max_value:
                return value
        print(f"Enter an integer in [{min_value}, {max_value}].")


def interactive_menu() -> None:
    print("=" * 72)
    print("LAB 4 LIVE VISUALIZATION - REAL-TIME DEMO")
    print("=" * 72)

    algorithm = _choose("Choose algorithm:", ["Dijkstra", "Floyd--Warshall"], default=0)
    graph_type = _choose("Choose graph type:", ["sparse", "dense"], default=0)
    size_default = 10 if algorithm == "Floyd--Warshall" else 14
    size_limit = 18 if algorithm == "Floyd--Warshall" else 24
    size = _ask_int("Graph size (keep small for live animation)", default=size_default, min_value=6, max_value=size_limit)
    interval = _ask_int("Animation interval in ms", default=400, min_value=50, max_value=2000)
    seed = _ask_int("Random seed", default=42, min_value=0, max_value=100000)

    print(f"\nLaunching {algorithm} on {graph_type} graph with N={size} ...")
    print("Close the Matplotlib window to finish.")

    config = LiveConfig(algorithm=algorithm, graph_type=graph_type, size=size, seed=seed, interval_ms=interval)
    LiveVisualizer(config).animate()


if __name__ == "__main__":
    interactive_menu()

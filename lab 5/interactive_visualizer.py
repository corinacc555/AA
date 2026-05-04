"""
interactive_visualizer.py - Real-time interactive visualization for Lab 5 (Prim & Kruskal).

This module provides a live demo for Prim's and Kruskal's algorithms
using Matplotlib animations, mirroring the style of the previous labs.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Dict, Generator, List, Optional, Set, Tuple

import matplotlib
try:
    matplotlib.use("TkAgg")
except Exception:
    pass
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import experiment
from algorithms import UnionFind


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def circular_layout(nodes: List[int]) -> Dict[int, Tuple[float, float]]:
    count = len(nodes)
    if count == 0:
        return {}
    positions = {}
    for index, vertex in enumerate(nodes):
        angle = 2.0 * math.pi * index / count
        positions[vertex] = (math.cos(angle), math.sin(angle))
    return positions


# ---------------------------------------------------------------------------
# Prim state generator
# ---------------------------------------------------------------------------

def prim_states(n: int, adj: Dict[int, List[Tuple[int, int]]], source: int = 0) -> Generator[dict, None, None]:
    visited: Set[int] = set()
    mst_edges: List[Tuple[int, int, int]] = []
    
    pq = [] # (weight, u, v)
    visited.add(source)
    for v, w in adj.get(source, []):
        heappush(pq, (w, source, v))
        
    yield {
        "step": 0,
        "visited": set(visited),
        "mst_edges": list(mst_edges),
        "pq_edges": [(u, v) for _, u, v in pq],
        "message": f"Initialized Prim from source {source}.",
    }

    step = 0
    while pq and len(mst_edges) < n - 1:
        step += 1
        w, u, v = heappop(pq)
        
        if v in visited:
            yield {
                "step": step,
                "visited": set(visited),
                "mst_edges": list(mst_edges),
                "pq_edges": [(u_, v_) for _, u_, v_ in pq],
                "message": f"Ignoring edge {u}-{v} (weight {w}) as {v} is already visited.",
            }
            continue
            
        visited.add(v)
        mst_edges.append((u, v, w))
        
        for to, wt in adj.get(v, []):
            if to not in visited:
                heappush(pq, (wt, v, to))
                
        yield {
            "step": step,
            "visited": set(visited),
            "mst_edges": list(mst_edges),
            "pq_edges": [(u_, v_) for _, u_, v_ in pq],
            "message": f"Added edge {u}-{v} (weight {w}) to MST. Visited {v}.",
        }

    yield {
        "step": step + 1,
        "visited": set(visited),
        "mst_edges": list(mst_edges),
        "pq_edges": [],
        "message": "Prim's algorithm completed.",
    }


# ---------------------------------------------------------------------------
# Kruskal state generator
# ---------------------------------------------------------------------------

def kruskal_states(n: int, edges: List[Tuple[int, int, int]]) -> Generator[dict, None, None]:
    uf = UnionFind(n)
    mst_edges: List[Tuple[int, int, int]] = []
    
    edges_sorted = sorted(edges)
    yield {
        "step": 0,
        "mst_edges": list(mst_edges),
        "eval_edge": None,
        "message": "Sorted edges by weight. Initialized Disjoint Set.",
    }

    step = 0
    for w, u, v in edges_sorted:
        step += 1
        
        ra, rb = uf.find(u), uf.find(v)
        if ra == rb:
            yield {
                "step": step,
                "mst_edges": list(mst_edges),
                "eval_edge": (u, v, w, False), # False means rejected
                "message": f"Edge {u}-{v} (weight {w}) rejected (forms cycle).",
            }
            continue
            
        uf.union(u, v)
        mst_edges.append((u, v, w))
        yield {
            "step": step,
            "mst_edges": list(mst_edges),
            "eval_edge": (u, v, w, True), # True means accepted
            "message": f"Edge {u}-{v} (weight {w}) accepted in MST.",
        }
        
        if len(mst_edges) == n - 1:
            break

    yield {
        "step": step + 1,
        "mst_edges": list(mst_edges),
        "eval_edge": None,
        "message": "Kruskal's algorithm completed.",
    }


# ---------------------------------------------------------------------------
# Live Animator
# ---------------------------------------------------------------------------

@dataclass
class LiveConfig:
    algorithm: str
    size: int = 15
    seed: int = 42
    interval_ms: int = 600

class LiveVisualizer:
    def __init__(self, config: LiveConfig) -> None:
        self.config = config
        random.seed(self.config.seed)
        self.adj, self.edges = experiment.generate_connected_graph(self.config.size, extra_edge_prob=0.1, weight_range=(1, 50))
        self.nodes = list(range(self.config.size))
        self.positions = circular_layout(self.nodes)
        
        self.anim = None
        self.fig, (self.ax_main, self.ax_text) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": [3, 1]})
        
        self.edge_lines = {}
        self.node_scatter = None

    def setup_plot(self) -> None:
        self.ax_main.set_title(f"{self.config.algorithm.title()} - Random Graph (N={self.config.size})", fontsize=13, fontweight="bold")
        self.ax_main.set_xticks([])
        self.ax_main.set_yticks([])
        self.ax_main.set_aspect("equal")

        self.ax_text.axis("off")
        self.ax_text.set_title("Algorithm Log", fontsize=12, fontweight="bold")

        x_coords = [self.positions[v][0] for v in self.nodes]
        y_coords = [self.positions[v][1] for v in self.nodes]

        # Draw all background edges
        for u in self.adj:
            for v, w in self.adj[u]:
                if u < v:
                    x0, y0 = self.positions[u]
                    x1, y1 = self.positions[v]
                    line, = self.ax_main.plot([x0, x1], [y0, y1], color="lightgray", zorder=1)
                    self.edge_lines[(u, v)] = line
                    # Draw weight text
                    self.ax_main.text((x0+x1)/2, (y0+y1)/2, str(w), color="gray", fontsize=8, zorder=2)

        # Draw nodes
        self.node_scatter = self.ax_main.scatter(x_coords, y_coords, s=200, c="lightblue", zorder=3, edgecolors="black")
        for v in self.nodes:
            self.ax_main.text(self.positions[v][0], self.positions[v][1], str(v), 
                              ha='center', va='center', fontsize=9, zorder=4)

        self.log_text = self.ax_text.text(0, 1, "", va="top", ha="left", fontsize=10, 
                                          wrap=True, bbox=dict(facecolor="white", edgecolor="none"))
        self.log_history = []

    def log(self, message: str) -> None:
        self.log_history.append(message)
        if len(self.log_history) > 15:
            self.log_history.pop(0)
        self.log_text.set_text("\\n".join(self.log_history))

    def update_prim(self, state: dict):
        visited = state.get("visited", set())
        mst_edges = state.get("mst_edges", [])
        
        colors = ["lightgreen" if v in visited else "lightblue" for v in self.nodes]
        self.node_scatter.set_facecolor(colors)
        
        mst_map = {(min(u,v), max(u,v)) for u,v,w in mst_edges}
        for (u, v), line in self.edge_lines.items():
            if (u, v) in mst_map:
                line.set_color("red")
                line.set_linewidth(3)
                line.set_zorder(2)
            else:
                line.set_color("lightgray")
                line.set_linewidth(1)
                line.set_zorder(1)
                
        if state["message"]:
            self.log(state["message"])
            
    def update_kruskal(self, state: dict):
        mst_edges = state.get("mst_edges", [])
        eval_edge = state.get("eval_edge", None)
        
        mst_map = {(min(u,v), max(u,v)) for u,v,w in mst_edges}
        for (u, v), line in self.edge_lines.items():
            if eval_edge and eval_edge[0] == u and eval_edge[1] == v:
                line.set_color("orange")
                line.set_linewidth(3)
            elif eval_edge and eval_edge[0] == v and eval_edge[1] == u:
                line.set_color("orange")
                line.set_linewidth(3)
            elif (u, v) in mst_map:
                line.set_color("red")
                line.set_linewidth(3)
            else:
                line.set_color("lightgray")
                line.set_linewidth(1)
                
        if state["message"]:
            self.log(state["message"])


    def animate(self):
        self.setup_plot()
        
        if self.config.algorithm.lower() == "prim":
            gen = prim_states(self.config.size, self.adj)
            update_func = self.update_prim
        else:
            gen = kruskal_states(self.config.size, self.edges)
            update_func = self.update_kruskal

        def render_frame(frame_data):
            update_func(frame_data)
            return self.ax_main, self.ax_text

        self.anim = animation.FuncAnimation(
            self.fig,
            render_frame,
            frames=gen,
            interval=self.config.interval_ms,
            repeat=False,
            cache_frame_data=False,
        )
        plt.tight_layout()
        plt.show()

def main() -> None:
    print("Select an algorithm to visualize:")
    print("1. Prim")
    print("2. Kruskal")
    choice = input("Enter choice (1-2): ").strip()
    algo = "prim" if choice == "1" else "kruskal"

    config = LiveConfig(algorithm=algo, size=15, interval_ms=500)
    visualizer = LiveVisualizer(config)
    visualizer.animate()

if __name__ == "__main__":
    main()

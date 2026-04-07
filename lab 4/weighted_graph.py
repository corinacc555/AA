"""
weighted_graph.py - Weighted graph structures and generators for Lab 4.

The graph is undirected and positively weighted, which is appropriate for
Dijkstra's algorithm and Floyd–Warshall.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class WeightedEdge:
    u: int
    v: int
    w: int


class WeightedGraph:
    """Undirected weighted graph represented as an adjacency list."""

    def __init__(self) -> None:
        self.adjacency_list: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        self.num_vertices: int = 0
        self.num_edges: int = 0
        self._vertices: List[int] = []
        self._edge_set: set[Tuple[int, int]] = set()

    def add_vertex(self, v: int) -> None:
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
            self._vertices.append(v)
            self.num_vertices += 1

    def add_edge(self, u: int, v: int, w: int) -> None:
        if u == v:
            return
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in self._edge_set:
            return
        self._edge_set.add((a, b))
        self.adjacency_list[u].append((v, w))
        self.adjacency_list[v].append((u, w))
        self.num_edges += 1

    def get_vertices(self) -> List[int]:
        return self._vertices

    def get_neighbors(self, v: int) -> List[Tuple[int, int]]:
        return self.adjacency_list[v]

    def __repr__(self) -> str:
        return f"WeightedGraph(V={self.num_vertices}, E={self.num_edges})"


class WeightedGraphGenerator:
    """Create connected sparse and dense graphs for empirical analysis."""

    @staticmethod
    def generate(graph_type: str, n: int, seed: int = 42) -> WeightedGraph:
        graph_type = graph_type.lower()
        if graph_type == "sparse":
            return WeightedGraphGenerator.sparse(n, seed)
        if graph_type == "dense":
            return WeightedGraphGenerator.dense(n, seed)
        raise ValueError(f"Unknown graph type: {graph_type}")

    @staticmethod
    def sparse(n: int, seed: int = 42) -> WeightedGraph:
        """Connected sparse graph: tree backbone + low-probability extra edges."""
        return WeightedGraphGenerator._connected_erdos_renyi(n, p=0.06, seed=seed)

    @staticmethod
    def dense(n: int, seed: int = 42) -> WeightedGraph:
        """Connected dense graph: tree backbone + high-probability extra edges."""
        return WeightedGraphGenerator._connected_erdos_renyi(n, p=0.35, seed=seed)

    @staticmethod
    def _connected_erdos_renyi(n: int, p: float, seed: int) -> WeightedGraph:
        rng = random.Random(seed)
        graph = WeightedGraph()
        for v in range(n):
            graph.add_vertex(v)

        # Ensure connectivity by first building a random spanning tree.
        for v in range(1, n):
            parent = rng.randint(0, v - 1)
            weight = rng.randint(1, 20)
            graph.add_edge(v, parent, weight)

        # Add extra edges according to density.
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < p:
                    weight = rng.randint(1, 20)
                    graph.add_edge(u, v, weight)

        return graph


GRAPH_TYPES = {
    "sparse": WeightedGraphGenerator.sparse,
    "dense": WeightedGraphGenerator.dense,
}

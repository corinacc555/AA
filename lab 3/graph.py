"""
graph.py - Graph data structure and graph generators for DFS/BFS analysis.

Provides an adjacency-list undirected Graph class and a GraphGenerator
with five distinct graph types used in the empirical study.
"""

import random
import math
from collections import defaultdict


class Graph:
    """Undirected graph represented as an adjacency list."""

    def __init__(self):
        self.adjacency_list: dict[int, list[int]] = defaultdict(list)
        self.num_vertices: int = 0
        self.num_edges: int = 0
        self._vertices: list[int] = []

    def add_vertex(self, v: int) -> None:
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
            self.num_vertices += 1
            self._vertices.append(v)

    def add_edge(self, u: int, v: int) -> None:
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
        self.num_edges += 1

    def get_vertices(self) -> list[int]:
        return self._vertices

    def get_neighbors(self, v: int) -> list[int]:
        return self.adjacency_list[v]

    def degree(self, v: int) -> int:
        return len(self.adjacency_list[v])

    def avg_degree(self) -> float:
        if self.num_vertices == 0:
            return 0.0
        return (2 * self.num_edges) / self.num_vertices

    def __repr__(self) -> str:
        return f"Graph(V={self.num_vertices}, E={self.num_edges})"


class GraphGenerator:
    """Factory methods that produce different graph types for empirical testing."""

    @staticmethod
    def random_sparse(n: int, seed: int = 42) -> Graph:
        """Erdős–Rényi G(n, p=0.05) — low edge density."""
        return GraphGenerator._erdos_renyi(n, p=0.05, seed=seed)

    @staticmethod
    def random_medium(n: int, seed: int = 42) -> Graph:
        """Erdős–Rényi G(n, p=0.1) — medium edge density."""
        return GraphGenerator._erdos_renyi(n, p=0.10, seed=seed)

    @staticmethod
    def random_dense(n: int, seed: int = 42) -> Graph:
        """Erdős–Rényi G(n, p=0.3) — high edge density."""
        return GraphGenerator._erdos_renyi(n, p=0.30, seed=seed)

    @staticmethod
    def _erdos_renyi(n: int, p: float, seed: int) -> Graph:
        rng = random.Random(seed)
        g = Graph()
        for i in range(n):
            g.add_vertex(i)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    g.add_edge(i, j)
        return g

    @staticmethod
    def tree(n: int, seed: int = 42) -> Graph:
        """Random spanning tree: each node i (i>0) is connected to a random
        node in [0, i-1]. Guarantees connectivity and exactly n-1 edges."""
        rng = random.Random(seed)
        g = Graph()
        for i in range(n):
            g.add_vertex(i)
        for i in range(1, n):
            parent = rng.randint(0, i - 1)
            g.add_edge(i, parent)
        return g

    @staticmethod
    def grid(n: int, seed: int = 42) -> Graph:
        """Square grid graph.  The grid side is ceil(sqrt(n)), so the actual
        vertex count is side*side >= n. Returns the full grid."""
        side = math.ceil(math.sqrt(n))
        actual_n = side * side
        g = Graph()
        for i in range(actual_n):
            g.add_vertex(i)
        for row in range(side):
            for col in range(side):
                v = row * side + col
                if col + 1 < side:
                    g.add_edge(v, v + 1)          # right neighbour
                if row + 1 < side:
                    g.add_edge(v, v + side)       # bottom neighbour
        return g


# Map of graph-type labels to generator callables
GRAPH_TYPES: dict[str, callable] = {
    "sparse":  GraphGenerator.random_sparse,
    "medium":  GraphGenerator.random_medium,
    "dense":   GraphGenerator.random_dense,
    "tree":    GraphGenerator.tree,
    "grid":    GraphGenerator.grid,
}

"""
dfs_bfs.py - Iterative DFS, Recursive DFS, and BFS with per-run metrics.

Each algorithm returns a SearchMetrics dataclass containing:
  - execution_time  : wall-clock time in seconds
  - nodes_visited   : total nodes popped/processed
  - edges_examined  : total neighbour lookups
  - max_memory      : peak stack / queue / recursion-depth size
  - visited_order   : list of nodes in traversal order
"""

import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import List

from graph import Graph


@dataclass
class SearchMetrics:
    execution_time: float = 0.0   # seconds
    nodes_visited: int = 0
    edges_examined: int = 0
    max_memory: int = 0           # peak stack/queue/depth size
    visited_order: List[int] = field(default_factory=list)

    def time_ms(self) -> float:
        return self.execution_time * 1000.0


# ─────────────────────────────────────────────────────────────────────────────
# DFS — Iterative (explicit stack)
# ─────────────────────────────────────────────────────────────────────────────

def dfs_iterative(graph: Graph, start: int) -> SearchMetrics:
    """
    Iterative DFS using an explicit stack.

    A node is pushed onto the stack when a neighbour is discovered for the
    first time; it is processed (marked visited + neighbours expanded) when
    popped.  max_memory = peak stack size.
    """
    m = SearchMetrics()
    t0 = time.perf_counter()

    visited = set()
    stack = [start]
    peak = 0

    while stack:
        if len(stack) > peak:
            peak = len(stack)
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        m.nodes_visited += 1
        m.visited_order.append(node)
        for neighbour in graph.get_neighbors(node):
            m.edges_examined += 1
            if neighbour not in visited:
                stack.append(neighbour)

    m.max_memory = peak
    m.execution_time = time.perf_counter() - t0
    return m


# ─────────────────────────────────────────────────────────────────────────────
# DFS — Recursive (call stack)
# ─────────────────────────────────────────────────────────────────────────────

def dfs_recursive(graph: Graph, start: int) -> SearchMetrics:
    """
    Classic recursive DFS.

    Python's default recursion limit is raised temporarily to handle large
    tree-like graphs where depth can equal the vertex count.
    max_memory = peak recursion depth.
    """
    m = SearchMetrics()
    visited = set()
    peak_depth = [0]

    def _dfs(node: int, depth: int) -> None:
        visited.add(node)
        m.nodes_visited += 1
        m.visited_order.append(node)
        if depth > peak_depth[0]:
            peak_depth[0] = depth
        for neighbour in graph.get_neighbors(node):
            m.edges_examined += 1
            if neighbour not in visited:
                _dfs(neighbour, depth + 1)

    old_limit = sys.getrecursionlimit()
    new_limit = max(old_limit, graph.num_vertices + 500)
    sys.setrecursionlimit(new_limit)
    t0 = time.perf_counter()
    try:
        _dfs(start, 0)
    finally:
        sys.setrecursionlimit(old_limit)

    m.max_memory = peak_depth[0]
    m.execution_time = time.perf_counter() - t0
    return m


# ─────────────────────────────────────────────────────────────────────────────
# BFS — Queue-based
# ─────────────────────────────────────────────────────────────────────────────

def bfs(graph: Graph, start: int) -> SearchMetrics:
    """
    Standard BFS using a double-ended queue.

    Nodes are marked visited when enqueued (not when dequeued) to avoid
    duplicate enqueueing.  max_memory = peak queue size.
    """
    m = SearchMetrics()
    t0 = time.perf_counter()

    visited = set([start])
    queue: deque[int] = deque([start])
    peak = 0

    while queue:
        if len(queue) > peak:
            peak = len(queue)
        node = queue.popleft()
        m.nodes_visited += 1
        m.visited_order.append(node)
        for neighbour in graph.get_neighbors(node):
            m.edges_examined += 1
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    m.max_memory = peak
    m.execution_time = time.perf_counter() - t0
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────────────────────

ALGORITHMS = {
    "DFS Iterative": dfs_iterative,
    "DFS Recursive": dfs_recursive,
    "BFS":           bfs,
}

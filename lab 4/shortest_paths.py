"""
shortest_paths.py - Dijkstra and Floyd–Warshall implementations for Lab 4.

Metrics collected:
  - execution_time_ms : wall-clock time in milliseconds
  - relaxations       : number of edge/cell checks
  - updates           : number of successful distance improvements
  - processed         : number of processed vertices (Dijkstra) or iterations
  - max_frontier      : peak heap/working-set size
"""

from __future__ import annotations

import heapq
import math
import time
from dataclasses import dataclass
from typing import List, Tuple

from weighted_graph import WeightedGraph


@dataclass
class PathMetrics:
    execution_time_ms: float = 0.0
    relaxations: int = 0
    updates: int = 0
    processed: int = 0
    max_frontier: int = 0


def dijkstra(graph: WeightedGraph, source: int = 0) -> Tuple[List[float], PathMetrics]:
    """Single-source shortest paths using a priority queue."""
    start = time.perf_counter()
    metrics = PathMetrics()
    n = graph.num_vertices
    dist = [math.inf] * n
    dist[source] = 0.0

    heap: List[Tuple[float, int]] = [(0.0, source)]
    visited = set()

    while heap:
        metrics.max_frontier = max(metrics.max_frontier, len(heap))
        current_distance, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        metrics.processed += 1

        if current_distance != dist[node]:
            continue

        for neighbour, weight in graph.get_neighbors(node):
            metrics.relaxations += 1
            candidate = current_distance + weight
            if candidate < dist[neighbour]:
                dist[neighbour] = candidate
                metrics.updates += 1
                heapq.heappush(heap, (candidate, neighbour))

    metrics.execution_time_ms = (time.perf_counter() - start) * 1000.0
    return dist, metrics


def floyd_warshall(graph: WeightedGraph) -> Tuple[List[List[float]], PathMetrics]:
    """All-pairs shortest paths using the dynamic programming formulation."""
    start = time.perf_counter()
    metrics = PathMetrics()
    n = graph.num_vertices

    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0

    for u in graph.get_vertices():
        for v, w in graph.get_neighbors(u):
            if w < dist[u][v]:
                dist[u][v] = float(w)

    # Standard Floyd–Warshall DP transition.
    for k in range(n):
        metrics.processed += 1
        for i in range(n):
            dik = dist[i][k]
            if dik == math.inf:
                continue
            for j in range(n):
                metrics.relaxations += 1
                candidate = dik + dist[k][j]
                if candidate < dist[i][j]:
                    dist[i][j] = candidate
                    metrics.updates += 1
        metrics.max_frontier = max(metrics.max_frontier, n)

    metrics.execution_time_ms = (time.perf_counter() - start) * 1000.0
    return dist, metrics

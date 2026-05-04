"""
Prim and Kruskal implementations for undirected weighted graphs.
Graph conventions used by the experiments:
- Nodes are 0..n-1
- For Prim: adjacency dict {u: [(v, w), ...]}
- For Kruskal: edge list [(w, u, v), ...]
"""
import heapq


def prim_mst(n, adj):
    """Return (total_weight, mst_edges)
    adj: dict node -> list of (neighbor, weight)
    """
    visited = [False] * n
    pq = []  # (weight, u, v)
    total = 0
    edges = []

    # start from node 0
    visited[0] = True
    for v, w in adj.get(0, []):
        heapq.heappush(pq, (w, 0, v))

    while pq and len(edges) < n - 1:
        w, u, v = heapq.heappop(pq)
        if visited[v]:
            continue
        visited[v] = True
        total += w
        edges.append((u, v, w))
        for to, wt in adj.get(v, []):
            if not visited[to]:
                heapq.heappush(pq, (wt, v, to))

    if len(edges) != n - 1:
        raise ValueError("Graph not connected")
    return total, edges


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        else:
            self.parent[rb] = ra
            if self.rank[ra] == self.rank[rb]:
                self.rank[ra] += 1
        return True


def kruskal_mst(n, edges):
    """edges: list of (weight, u, v)
    Return (total_weight, mst_edges)
    """
    uf = UnionFind(n)
    mst = []
    total = 0
    edges_sorted = sorted(edges)
    for w, u, v in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break
    if len(mst) != n - 1:
        raise ValueError("Graph not connected")
    return total, mst

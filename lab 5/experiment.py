"""
Generate random connected graphs, run Prim and Kruskal, record runtimes.
Produces CSV: results.csv with columns: n, run, algorithm, time_seconds, total_weight
"""
import random
import time
import csv
import algorithms


def generate_connected_graph(n, extra_edge_prob=0.05, weight_range=(1, 100)):
    """Create connected undirected graph as adjacency dict and edge list.
    Approach: first create a random spanning tree, then add extra edges with probability p.
    Returns: adj (dict), edges (list of (w,u,v))
    """
    nodes = list(range(n))
    adj = {i: [] for i in nodes}
    edges = []

    # Create random spanning tree
    parents = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        w = random.randint(*weight_range)
        adj[u].append((v, w))
        adj[v].append((u, w))
        edges.append((w, u, v))

    # Add extra random edges
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < extra_edge_prob:
                w = random.randint(*weight_range)
                adj[u].append((v, w))
                adj[v].append((u, w))
                edges.append((w, u, v))

    return adj, edges


def run_experiments(node_counts=None, runs_per_setting=3, p=0.05):
    if node_counts is None:
        node_counts = [100, 200, 400, 800]

    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'run', 'algorithm', 'time_seconds', 'total_weight'])

        for n in node_counts:
            for run in range(1, runs_per_setting + 1):
                adj, edges = generate_connected_graph(n, extra_edge_prob=p)

                # Kruskal (use edges list)
                t0 = time.perf_counter()
                total_k, _ = algorithms.kruskal_mst(n, edges)
                t1 = time.perf_counter()
                writer.writerow([n, run, 'kruskal', t1 - t0, total_k])

                # Prim (use adj)
                t0 = time.perf_counter()
                total_p, _ = algorithms.prim_mst(n, adj)
                t1 = time.perf_counter()
                writer.writerow([n, run, 'prim', t1 - t0, total_p])

                print(f"n={n} run={run} kruskal={t1 - t0:.6f} prim={t1 - t0:.6f}")


if __name__ == '__main__':
    run_experiments()

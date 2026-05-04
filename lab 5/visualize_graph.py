"""
Interactive graph + MST visualization using pyvis.
Generates `graph_mst.html` showing the generated graph and highlights the MST edges.
"""
from pyvis.network import Network
import networkx as nx
import experiment
import algorithms


def visualize_sample(n=30, out_html='graph_mst.html'):
    adj, edges = experiment.generate_connected_graph(n, extra_edge_prob=0.08, weight_range=(1,50))

    # Build networkx graph
    G = nx.Graph()
    for u in adj:
        for v, w in adj[u]:
            if u < v:
                G.add_edge(u, v, weight=w)

    # Compute MST (Kruskal)
    edge_list = [(w, u, v) for (u, nbrs) in adj.items() for (v, w) in nbrs if u < v]
    total, mst_edges = algorithms.kruskal_mst(n, edge_list)
    mst_set = set((min(u,v), max(u,v)) for u,v,w in mst_edges)

    net = Network(height='800px', width='100%', notebook=False)
    net.barnes_hut()

    for node in G.nodes():
        net.add_node(node, label=str(node))

    for u, v, data in G.edges(data=True):
        w = data.get('weight', 1)
        key = (min(u,v), max(u,v))
        if key in mst_set:
            net.add_edge(u, v, value=w, title=str(w), color='red', width=3)
        else:
            net.add_edge(u, v, value=w, title=str(w))

    net.show(out_html)
    print('Saved interactive graph to', out_html)


if __name__ == '__main__':
    visualize_sample()

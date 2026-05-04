"""
Load results.csv and plot mean runtime vs n for Prim and Kruskal.
Produces: time_vs_nodes.png
"""
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


def load_results(fname='results.csv'):
    data = defaultdict(lambda: defaultdict(list))  # data[n][algo] -> list(times)
    with open(fname, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row['n'])
            algo = row['algorithm']
            t = float(row['time_seconds'])
            data[n][algo].append(t)
    return data


def plot(data, out='time_vs_nodes.png'):
    nodes = sorted(data.keys())
    prim_means = []
    kruskal_means = []
    for n in nodes:
        prim = data[n].get('prim', [])
        kruskal = data[n].get('kruskal', [])
        prim_means.append(sum(prim) / len(prim) if prim else 0)
        kruskal_means.append(sum(kruskal) / len(kruskal) if kruskal else 0)

    plt.figure()
    plt.plot(nodes, prim_means, marker='o', label='Prim')
    plt.plot(nodes, kruskal_means, marker='o', label='Kruskal')
    plt.xlabel('Number of nodes (n)')
    plt.ylabel('Mean time (s)')
    plt.title('Prim vs Kruskal: runtime vs nodes')
    plt.legend()
    plt.grid(True)
    plt.savefig(out, dpi=200)
    print('Saved plot to', out)


if __name__ == '__main__':
    data = load_results()
    plot(data)

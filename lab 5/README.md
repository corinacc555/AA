AA Lab 5 — Prim and Kruskal

Files:
- `algorithms.py` — Prim and Kruskal implementations
- `experiment.py` — graph generation and experiment runner (writes `results.csv`)
- `plot_results.py` — aggregate `results.csv` and save `time_vs_nodes.png`
- `main.py` — small CLI wrapper

Quick start:

1. Create a virtualenv and install deps:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Run experiments (may take some time for larger n):

```powershell
python experiment.py
```

3. Produce plots (static PNG):

```powershell
python plot_results.py
```

4. Produce an interactive runtime plot (HTML):

```powershell
python plot_interactive.py
```

5. Visualize a sample graph and its MST interactively (HTML):

```powershell
python visualize_graph.py
```

Notes:
- You can edit `experiment.py` to change `node_counts` or `runs_per_setting`.
- Results are written to `results.csv` in this folder.

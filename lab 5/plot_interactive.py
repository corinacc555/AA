"""
Create an interactive HTML plot (Plotly) of mean runtime vs nodes.
Generates `time_vs_nodes_interactive.html` from `results.csv`.
"""
import pandas as pd
import plotly.express as px


def main(csv_path='results.csv', out_html='time_vs_nodes_interactive.html'):
    df = pd.read_csv(csv_path)
    agg = df.groupby(['n', 'algorithm'], as_index=False)['time_seconds'].mean()
    fig = px.line(agg, x='n', y='time_seconds', color='algorithm', markers=True,
                  labels={'n': 'Number of nodes', 'time_seconds': 'Mean time (s)'},
                  title='Prim vs Kruskal: mean runtime vs nodes')
    fig.update_layout(template='plotly_white')
    fig.write_html(out_html, full_html=True)
    print('Saved interactive plot to', out_html)


if __name__ == '__main__':
    main()

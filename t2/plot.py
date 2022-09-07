# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import math
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

def read_dat(b):
    with open(f"data/time.{b}.dat") as f:
        return list(map(float, f.read().split()))

fig = go.Figure()
# b = 64
# while b <= 2048:
#     fig.add_trace(go.Histogram(x=read_dat(b), name=f"{b} bits"))
#     b *= 2
fig.add_trace(go.Histogram(x=read_dat(2048), opacity=0.4, name=f"2048 bits"))
fig.update_layout(barmode='stack')

app.layout = html.Div(children=[
    dcc.Graph(
        figure=fig
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)


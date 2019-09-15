import os
from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output

import pandas as pd
import plotly.graph_objs as go
import math
import json

# def register_callbacks(dashapp):
#     @dashapp.callback(Output('example-graph', 'figure'))
#     def update_graph(selected_dropdown_value):
#         print("test 1")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def register_callbacks(dashapp):
    @dashapp.callback(
            Output('bubble-graph', 'figure'),
            [Input('hidden','value')]
        )
    def update_graph(hidden):
        path = os.path.join(BASE_DIR, 'temp_data.json')
        openfile=open(path, 'r')
        jsondata=json.load(openfile)
        df=pd.DataFrame(jsondata)

        openfile.close()
        max_msgs = df['max_total_msgs'][0]

        # df = pd.read_json('./temp_data.json', lines = True)
        fig = go.Scatter(
            x = [0, 200, -160, 0, 0, 110, -90, 110, -80, 80, -100, 200, 200, -175, 100, 175, 200, 100, -100, -180, -175, -175],
            y = [0, 0, 10, 160, -150, 30, 90, -80, -90, 110, 175, 100, -200, -150, -175, 160, -100, 190, -200, -83, 100, 170],
            text = [(convo['conv_name'] + '<br>' + str(convo['statistics']['total_msg_count'])) for convo in df['conversation_data']],
            textposition="middle center",
            hoverinfo="none",
            mode='markers + text',
            opacity=0.7,
            marker={
                'size': [200, 150, 150, 120, 120, 120, 120, 120, 120, 100, 90, 90, 90, 90, 80, 70, 70, 70, 70, 60, 50, 50, 50],
                'line': {'width': 0.5, 'color': 'white'}
            },
            showlegend = False,
            name="name",
            textfont=dict(
                family = "Arial", 
                size = 18, 
                color = "black"
            )
        ),
        layout = go.Layout(
            height=900, 
            xaxis={
                'title': 'x-axis',
                'type': 'linear', #if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'y-axis ',
                'type': 'linear', #if yaxis_type == 'Linear' else 'log'
            }
        )

        return {'data':fig}
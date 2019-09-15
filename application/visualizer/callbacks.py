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
            x = [int(convo['statistics']['total_msg_count']) for convo in df['conversation_data']],#['gdp per capita'],
            y = [int(convo['participant_count']) for convo in df['conversation_data']],#['life expectancy'],
            text = [convo['conv_name'] for convo in df['conversation_data']],
            mode='markers',
            opacity=0.7,
            marker={
                'size': [20*math.sqrt((256/max_msgs)*int(convo['statistics']['total_msg_count'])) for convo in df['conversation_data']],
                'line': {'width': 0.5, 'color': 'white'}
            },
            showlegend = False,
            name="name"
        ),
        layout = go.Layout(
            xaxis={
                'title': 'x-axis',
                'type': 'linear' #if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'y-axis ',
                'type': 'linear' #if yaxis_type == 'Linear' else 'log'
            }
        )
        return {'data':fig}
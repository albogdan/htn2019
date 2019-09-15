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


# def register_callbacks(dashapp):
#     @dashapp.callback(
#             Output('bubble-graph', 'figure'),
#             [Input('hidden','value')]
#         )
#     def update_graph(hidden):
#         path = os.path.join(BASE_DIR, 'temp_data.json')
#         openfile=open(path, 'r')
#         jsondata=json.load(openfile)
#         df=pd.DataFrame(jsondata)

#         openfile.close()
#         max_msgs = df['max_total_msgs'][0]

#         # df = pd.read_json('./temp_data.json', lines = True)
#         fig = go.Scatter(
#             x = [0, 200, -160, 0, 0, 110, -90, 110, -80, 80, -100, 200, 200, -175, 100, 175, 200, 100, -100, -180, -175, -175],
#             y = [0, 0, 10, 160, -150, 30, 90, -80, -90, 110, 175, 100, -200, -150, -175, 160, -100, 190, -200, -83, 100, 170],
#             text = [(convo['conv_name'] + '<br>' + str(convo['statistics']['total_msg_count'])) for convo in df['conversation_data']],
#             textposition="middle center",
#             hoverinfo="none",
#             mode='markers + text',
#             opacity=0.7,
#             marker = dict(
#                 color = ['blue', 'blue', 'blue', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow'],
#                 size = [200, 150, 150, 120, 120, 120, 120, 120, 120, 100, 90, 90, 90, 90, 80, 70, 70, 70, 70, 60, 50, 50, 50],
#                 line=dict(color = 'white', width = 0.5)
#             ),
#             showlegend = False,
#             name="name",
#             textfont=dict(
#                 family = "Arial", 
#                 size = [18, 18, 18, 16, 16, 16, 16, 16, 16, 16, 14, 14, 14, 14, 12, 10, 10, 10, 10, 10, 10, 10, 10], 
#                 color = "black"
#             )
#         ),
#         layout = go.Layout(
#             # xaxis=dict(zeroline=False,showgrid=False),
#             # yaxis=dict(zeroline=False,showgrid=False)
#         )

#         return {'data':fig}


# def register_callbacks(dashapp):
#     @dashapp.callback(
#             Output('profanity', 'figure'),
#             [Input('hidden','value')]
#         )
#     def update_graph(hidden2):
#         path = os.path.join(BASE_DIR, 'temp_data_profanity.json')
#         openfile=open(path, 'r')
#         jsondata=json.load(openfile)
#         df=pd.DataFrame(jsondata)

#         openfile.close()
#         max_msgs = df['max_total_msgs'][0]

#         # df = pd.read_json('./temp_data.json', lines = True)
#         fig = go.Bar(
#             x = [(convo['conv_name']) for index,convo in zip(range(12), df['conversation_data'])],
#             y = [convo['statistics']['total_profanity_count'] for convo in df['conversation_data']],
#             hovertext = [convo['statistics']['total_profanity_count'] for convo in df['conversation_data']],
#             hoverinfo="text",
#         ),
#         layout = go.Layout(
#         )

#         return {'data':fig}



def register_callbacks(dashapp):
    @dashapp.callback(
            Output('abbreviation', 'figure'),
            [Input('hidden','value')]
        )
    def update_graph(hidden2):
        path = os.path.join(BASE_DIR, 'temp_data_abbreviation.json')
        openfile=open(path, 'r')
        jsondata=json.load(openfile)
        df=pd.DataFrame(jsondata)

        openfile.close()
        max_msgs = df['max_total_msgs'][0]

        # df = pd.read_json('./temp_data.json', lines = True)
        fig = go.Bar(
            x = [(convo['conv_name']) for index,convo in zip(range(12), df['conversation_data'])],
            y = [convo['statistics']['total_abbreviation_count'] for convo in df['conversation_data']],
            hovertext = [convo['statistics']['total_abbreviation_count'] for convo in df['conversation_data']],
            hoverinfo="text",
        ),
        layout = go.Layout(
        )

        return {'data':fig}
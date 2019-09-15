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
        
        #df = pd.read_json('./temp_data.json', lines = True)
        fig = go.Scatter(
            x = [0, 200, -160, 0, 0, 110, -90, 110, -80, 80, -100, 200, 200, -175, 100, 175, 200, 100, -100, -180, -175, -175],
            y = [0, 0, 10, 160, -150, 30, 90, -80, -90, 110, 175, 100, -200, -150, -175, 160, -100, 190, -200, -83, 100, 170],
            text = [(convo['conv_name'] + '<br>' + str(convo['statistics']['total_msg_count'])) for convo in df['conversation_data']],
            textposition="middle center",
            hoverinfo="none",
            mode='markers + text',
            opacity=0.7,
            marker = dict(
                color = ['blue', 'blue', 'blue', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow'],
                size = [200, 150, 150, 120, 120, 120, 120, 120, 120, 100, 90, 90, 90, 90, 80, 70, 70, 70, 70, 60, 50, 50, 50],
                line=dict(color = 'white', width = 0.5)
            ),
            showlegend = False,
            name="name",
            textfont=dict(
                family = "Arial", 
                size = [18, 18, 18, 16, 16, 16, 16, 16, 16, 16, 14, 14, 14, 14, 12, 10, 10, 10, 10, 10, 10, 10, 10], 
                color = "black"
            )
        ),
        layout = go.Layout(
            # xaxis=dict(zeroline=False,showgrid=False),
            # yaxis=dict(zeroline=False,showgrid=False)
        )

        return {'data':fig}

    @dashapp.callback(
            Output('profanity', 'figure'),
            [Input('hidden_profanity','value')]
        )
    def update_graph_profanity(hidden):
        path_profanity = os.path.join(BASE_DIR, 'temp_data_profanity.json')
        openfile_profanity=open(path_profanity, 'r')
        jsondata_profanity=json.load(openfile_profanity)
        df_profanity=pd.DataFrame(jsondata_profanity)

        openfile_profanity.close()

        fig_profanity = go.Bar(
            x = [(convo['conv_name']) for index,convo in zip(range(12), df_profanity['conversation_data'])],
            y = [convo['statistics']['total_profanity_count'] for convo in df_profanity['conversation_data']],
            text = [round(convo['statistics']['total_profanity_count'],2) for convo in df_profanity['conversation_data']],
            textposition="outside",
            hoverinfo="text",
            hovertext=[breakdown(convo, 'profanity') for convo in df_profanity['conversation_data']],
            opacity=0.7,
            marker = dict(
                color = 'pink', 
                line=dict(color = 'white', width = 0.5)
            )
        ),
        layout = go.Layout(
        )

        return {'data':fig_profanity}

    @dashapp.callback(
            Output('abbreviation', 'figure'),
            [Input('hidden_abb','value')]
        )
    def update_graph_abb(hidden):
        path_abb = os.path.join(BASE_DIR, 'temp_data_abbreviation.json')
        openfile_abb=open(path_abb, 'r')
        jsondata_abb=json.load(openfile_abb)
        df_abb=pd.DataFrame(jsondata_abb)

        openfile_abb.close()

        fig_abb = go.Bar(
            x = [(convo['conv_name']) for index,convo in zip(range(12), df_abb['conversation_data'])],
            y = [convo['statistics']['total_abbreviation_count'] for convo in df_abb['conversation_data']],
            text = [round(convo['statistics']['total_abbreviation_count'],2) for convo in df_abb['conversation_data']],
            textposition="outside",
            hoverinfo="text",
            hovertext=[breakdown(convo, 'abbreviation') for convo in df_abb['conversation_data']],
            opacity=0.7,
            marker = dict(
                color = 'blue', 
                line=dict(color = 'white', width = 0.5)
            )
        ),
        layout = go.Layout(
        )

        return {'data':fig_abb}

    @dashapp.callback(
            Output('positive_sentiment', 'figure'),
            [Input('hidden_pos','value')]
        )
    def update_graph_pos(hidden):
        path_pos = os.path.join(BASE_DIR, 'temp_data_sentiment.json')
        openfile_pos=open(path_pos, 'r')
        jsondata_pos=json.load(openfile_pos)
        df_pos=pd.DataFrame(jsondata_pos)

        openfile_pos.close()

        fig_pos = go.Bar(
            x = [(convo['conv_name']) for index,convo in zip(range(12), df_pos['conversation_data'])],
            y = [convo['statistics']['total_sentiment'] for convo in df_pos['conversation_data']],
            text = [round(convo['statistics']['total_sentiment'],2) for convo in df_pos['conversation_data']],
            textposition="outside",
            hoverinfo="text",
            hovertext=[breakdown(convo, 'positive') for convo in df_pos['conversation_data']],
            opacity=0.7,
            marker = dict(
                color = 'green', 
                line=dict(color = 'white', width = 0.5)
            )
        ),
        layout = go.Layout(
        )
        return {'data':fig_pos}

    @dashapp.callback(
            Output('negative_sentiment', 'figure'),
            [Input('hidden_neg','value')]
        )
    def update_graph_neg(hidden):
        path_neg = os.path.join(BASE_DIR, 'temp_data_sentiment_negative.json')
        openfile_neg=open(path_neg, 'r')
        jsondata_neg=json.load(openfile_neg)
        df_neg=pd.DataFrame(jsondata_neg)

        openfile_neg.close()
       
        fig_neg = go.Bar(
            x = [(convo['conv_name']) for index,convo in zip(range(12), df_neg['conversation_data'])],
            y = [convo['statistics']['total_sentiment'] for convo in df_neg['conversation_data']],
            text = [round(convo['statistics']['total_sentiment'],2) for convo in df_neg['conversation_data']],
            textposition="outside",
            hoverinfo="none",
            opacity=0.7,
            marker = dict(
                color = 'red', 
                line=dict(color = 'white', width = 0.5)
            )
        ),
        layout = go.Layout(
        )
        return {'data':fig_neg}


def breakdown(convo, mode):
    toReturn = ''; 

    for sender in convo['participants']:
        if (mode == 'profanity'):
            toReturn = toReturn + str(sender) + ": " + str(convo['participants'][sender]['profanity_count']) + "<br>"
        elif(mode == 'abbreviation'):
            toReturn = toReturn + str(sender) + ": " + str(convo['participants'][sender]['abbreviation_count']) + "<br>"
        elif(mode == 'positive' or mode == 'negative'): 
            toReturn = toReturn + str(sender) + ": " + str(round(convo['participants'][sender]['sentiment'],2)) + "<br>"

    return toReturn; 
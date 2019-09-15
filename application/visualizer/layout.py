import plotly.graph_objects as go
import datetime
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
colors = {
    'background': '#0',
    'text': '#7FDBFF'
}

layout = html.Div(style={'backgroundColor':colors['background']}, children=[
    html.H1(
        children='My Network',
        style={
            'textAlign': 'center',
            'color': 'black'
        }

    ),
    html.H4(
        children='The friends and groups you engage with most.',
        style={
            'textAlign': 'center',
            'color':colors['text']
        }

    ),

    # html.Div(children='Dash: A web application framework for Python.',
    #     style={
    #         'textAlign': 'center',
    #         'color':colors['text']
    #     }
    # ),

    # html.Div([
    #     dcc.Graph(id='bubble-graph', style={'height':900}),
    #     dcc.Input(id='hidden', type='hidden')
    # ]), 

    # html.A('Test', href='https://www.surveymonkey.com', style={'font':'12px Helvetica, sans-serif', 
    #                                                            'color': '#999', 'text-decoration': 'none'}),
	# html.Script(type='text/javascript', children='./survey.js')

    html.H1(
        children='Profanity Check',
        style={
            'textAlign': 'center',
            'color':'black'
        }

    ),
    html.H4(
        children='Everyone has a potty mouth. How bad is yours?',
        style={
            'textAlign': 'center',
            'color':colors['text']
        }

    ),
    
    # html.Div([
    #     dcc.Graph(id='profanity', style={'height':600}),
    #     dcc.Input(id='hidden', type='hidden')
    # ]) , 



    html.H1(
        children='Abbreviation Check',
        style={
            'textAlign': 'center',
            'color':'black'
        }

    ),
    html.H4(
        children='LOL. BRB. TY. How often do you and your friends abbreviate in your messages?',
        style={
            'textAlign': 'center',
            'color':colors['text']
        }

    ),
    
    # html.Div([
    #     dcc.Graph(id='abbreviation', style={'height':600}),
    #     dcc.Input(id='hidden', type='hidden')
    # ]),   
    
    
    
    html.H1(
        children='Positive Sentiment',
        style={
            'textAlign': 'center',
            'color':'black'
        }

    ),
    html.H4(
        children='How positive are you in your messages with your friends?',
        style={
            'textAlign': 'center',
            'color':colors['text']
        }

    ),
    
    html.Div([
        dcc.Graph(id='positive_sentiment', style={'height':600}),
        dcc.Input(id='hidden', type='hidden')
    ]),


    html.H1(
        children='Negative Sentiment',
        style={
            'textAlign': 'center',
            'color':'black'
        }

    ),
    html.H4(
        children='How negative are you in your messages with your friends?',
        style={
            'textAlign': 'center',
            'color':colors['text']
        }

    ),
    
    html.Div([
        dcc.Graph(id='negative_sentiment', style={'height':600}),
        dcc.Input(id='hidden_negative_sentiment', type='hidden')
    ])          

])
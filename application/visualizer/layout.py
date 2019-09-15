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
            'color':colors['text']
        }

    ),

    # html.Div(children='Dash: A web application framework for Python.',
    #     style={
    #         'textAlign': 'center',
    #         'color':colors['text']
    #     }
    # ),

    html.Div([
        dcc.Graph(id='bubble-graph', style={'height':900}),
        dcc.Input(id='hidden', type='hidden')
    ])    

    # html.Div([
    #     dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
    #         <script>(function(t,e,s,n){var o,a,c;t.SMCX=t.SMCX||[],e.getElementById(n)||(o=e.getElementsByTagName(s),a=o[o.length-1],c=e.createElement(s),c.type="text/javascript",c.async=!0,c.id=n,c.src=["https:"===location.protocol?"https://":"http://","widget.surveymonkey.com/collect/website/js/tRaiETqnLgj758hTBazgd7WnuXmrKllSQSuChpOpd0l8AutWppLPTnkxqDkGVIZL.js"].join(""),a.parentNode.insertBefore(c,a))})(window,document,"script","smcx-sdk");</script>
	#         <a style="font: 12px Helvetica, sans-serif; color: #999; text-decoration: none;" href=https://www.surveymonkey.com> Create your own user feedback survey </a>
    #     '''),
    # ])

])
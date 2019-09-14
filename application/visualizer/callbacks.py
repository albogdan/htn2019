from datetime import datetime as dt

from dash.dependencies import Input
from dash.dependencies import Output


def register_callbacks(dashapp):
    @dashapp.callback(Output('example-graph', 'figure'))
    def update_graph(selected_dropdown_value):
        print("test 1")

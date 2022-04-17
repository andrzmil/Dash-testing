from fileinput import filename
from turtle import width
from dash import Dash, html, dcc, dash_table, Input, Output, State
from tkinter.filedialog import askopenfilename
from dash.exceptions import PreventUpdate
import random

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions=True



app.layout = html.Div(children=[
    html.H1(children='Automatching Viewer'),
    
    html.Div(children=[
        html.Button(children='CREATE NEW PROJECT', id='create-new'),
        html.Button(children = 'LOAD EXISTING PROJECT', id='load-existing')
        
        
    ], style={'width': '100%'}, id='buttons-bar'),
    
    html.Div(children=[], id='input-div'),
    
    html.Div(children=[], id='outputs-div', style={'display': 'flex'})
    
])




####CALLBACKS
@app.callback(
    Output('input-div', 'children'),
    Input('create-new', 'n_clicks')    
)
def on_button_click(button_clicks):
    global ids
    if button_clicks is None:
        raise PreventUpdate
    else:
        
        fl = askopenfilename()
        if fl:
            df = pd.read_csv(fl)
            ids = list(set(df['YEAR'])) 
            
            children = [
                dcc.Dropdown(options= {'TM': 'TO MATCH', 'DF': 'DEFERRED'}, id='status'),
                dcc.Dropdown(options=ids, id='choose-id'),
                html.Button(children='MATCH', id='match-button', style={'width': '30%'}),
                html.Button(children='DEFER', id='defer-button'),
                html.Button(children='EXPORT', id='export-button')
                    
                    ]
            return children
        else:
            pass

   
@app.callback(
    Output('outputs-div', 'children'),
    Input('choose-id', 'value')    
)
def on_change_id(value):
    if value is None:
        raise PreventUpdate
    else:
        children_id = [
            html.Div(children=[
                html.Label(children='TITLE TO MATCH'),
                dcc.RadioItems(options=[i for i in [random.random() for i in range(50)]], id='selected-title')
                ], style={"width":"20%"}),
            
            html.Div(children=[], id='authors-div')
        ]
        return children_id

####################SHOW AUTHORS   
@app.callback(
    Output('authors-div', 'children'),
    Input('selected-title', 'value')
)
def on_change_title(value):
    if value is None:
        raise PreventUpdate
    else:
        children_author = [html.Li(children=li) for li in [random.random() for i in range(4)]]
        return children_author



if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_ui=False,dev_tools_props_check=False)
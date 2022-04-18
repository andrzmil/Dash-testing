
from dash import Dash, html, dcc, Input, Output
from tkinter.filedialog import askopenfilename
from dash.exceptions import PreventUpdate
from dash import callback_context
import random

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)
app.config.suppress_callback_exceptions=True



app.layout = html.Div(children=[
    html.H1(children='Automatching Viewer', style={'background':'black', 'color':'white'}),
    
    html.Div(children=[
        html.Button(children='CREATE NEW PROJECT', id='create-new'),
        html.Button(children = 'LOAD EXISTING PROJECT', id='load-existing')
        
        
    ], style={'width': '100%', "background": "cornflowerblue"}, id='buttons-bar'),
    
    html.Div(children=[], id='input-div', style={"background": "cornflowerblue"}),
    
    html.Div(children=[], id='outputs-div', style={'display': 'flex'})
    
])




####CALLBACKS


###########ON create button click - refresh input div or on create + additionaly on close project
@app.callback(
    Output('input-div', 'children'),
    Input('create-new', 'n_clicks')    
)
def on_button_click(button_clicks):
    if button_clicks is None:
        raise PreventUpdate
    else:
        
        fl = askopenfilename()
        if fl:
            df = pd.read_csv(fl)
            ids = list(set(df['YEAR'])) 
            
            children = [
                dcc.RadioItems(options= {'TM': 'TO MATCH', 'DF': 'DEFERRED'}, id='status', value="TM"),
                dcc.Dropdown(options=ids, id='choose-id', value=ids[0]),
                html.Button(children='MATCH', id='match-button', style={'width': '30%'}),
                html.Button(children='DEFER', id='defer-button'),
                html.Button(children='EXPORT', id='export-button')
                    
                    ]
            del(fl)
            return children
        else:
            children = []
            return children
        
        




#############callback on change id from dropdownlist   
############affects both - input list (choose_id_value) and status (to_match/deferred - status_value) 
@app.callback(
    Output('outputs-div', 'children'),
    [Input('choose-id', 'value'),
     Input('status', 'value')]    
)
def on_change_id(choose_id_value, status_value):
    #if choose_id_value or status_value is None:
    #    raise PreventUpdate
    #else:
    
        if choose_id_value:
            children_id = [
            html.Div(children=[
                html.Label(children='TITLE TO MATCH', id='title-to-match'),
                dcc.RadioItems(options=[i for i in [random.random() for i in range(50)]], id='selected-title')
                ], style={"width":"20%", "overflow-x":"hidden", "overflow-y":"auto", "height": "600px", "background": "grey"}),
            
            html.Div(children=[], id='authors-div', style={"background": "yellow", "width": "40%"})
            ]
        elif status_value:
            children_id = [
            html.Div(children=[
                html.Label(children='TITLE TO MATCH', id='title-to-match'),
                dcc.RadioItems(options=[i for i in [random.random() for i in range(20)]], id='selected-title')
                ], style={"width":"20%", "overflow-x":"hidden", "overflow-y":"auto", "height": "600px", "background": "grey"}),
            
            html.Div(children=[], id='authors-div', style={"background": "yellow", "width": "40%"})
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
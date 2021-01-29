import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import JsonStockData
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_table
import datetime
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np
app = dash.Dash(__name__)



base = JsonStockData.JsonStockData()
stock_df = base.stock_df
output= list()
for stock in ['0050', '2330', '00881']:
    df = stock_df[stock]
    df["No"] = len(df)*[stock]
    output.append(df)
df = pd.concat(output)
    
    

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-row-ids',
        columns=[{'name': i, 'id': i} for i in df.columns if i != 'id'],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        page_action='native',
        page_current= 0,
        page_size= 40,
    ),
    html.Div(id='datatable-row-ids-container')
])





@app.callback(
    Output('datatable-row-ids-container', 'children'),
    Input('datatable-row-ids', 'derived_virtual_row_ids'))
def update_graphs(row_ids):
    fig = px.scatter_matrix(df,
        dimensions=["Rate", "Open"],
        color="No")
    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=True)


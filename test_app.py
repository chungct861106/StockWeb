import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
sets = dict()
stock_df = dict()
with open("StockDataBase.json", encoding="utf-8") as f:
    Info = json.load(f)
    stocks = Info['stocks']
    if len(Info['sets']) > 0:
        sets = Info['sets']
        for stock in stocks:
            stock_df[stock] = pd.DataFrame(stocks[stock])
            

choosen = ['0050', '00876']
max_date = '2021-01-01'
min_date = '2020-01-01'
limit_month = [1, 2, 10, 12]
limit_weekday = ['Monday','Wensday', 'Friday']
output = list()
for stock in choosen:
    df = stock_df[stock]
    df['Date'] = df.index
    df = df.loc[(df['Date']<max_date) & (df['Date']>min_date)]
    mask1 = [day in limit_weekday for day in df['weekday']]
    df = df.loc[mask1]
    mask2 = [month in limit_month for month in df['month']]
    df = df.loc[mask2]
    df['No'] = [stock]*len(df)
    col = ['Date','No','Open', 'Close', 'High', 'Low', 'Margin buy', 'Margin sell', 'Short buy', 'Short sell', 'Total net add', 'Rate']
    df = df.filter(col)
    df["Rate"] = [ "%.2f%%" % (num*100) for num in df['Rate']]
    output.append(df)
df =  pd.concat(output)

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[{"name": i, "id": i} for i in col],
    page_size=30,
    fixed_columns={'headers':True},
    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'textAlign': 'left'
    },
    fixed_rows={'headers': True},
    style_table={'height': '300px', 'overflowY': 'auto'},
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
)

app.run_server(debug=True)
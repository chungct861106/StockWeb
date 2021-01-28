import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_table
import datetime
import JsonStockData
import pandas as pd

base = JsonStockData.JsonStockData()
current_options = []
today = datetime.datetime.today()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

Sets = [
    html.H6("Select Sets"),
    dcc.Dropdown(id='select-sets-input',
            options = [{'label': key, 'value': key} for key in base.sets],
            placeholder="Select a set", searchable=False),
    html.H6("New Sets", id='new-set-name'),
    html.Div([
        dcc.Input(value='TNew Sets Name', type='text', id='new-sets-input', style={'float':'left'}, autoComplete='off'),
        html.Button(id='submit-new-sets', n_clicks=0, children='Create Sets', style={'float':'right'})],
        style={'height':'32px'}),
    html.H6("Delete Sets", id='del-set-name'),
    html.Div([
        dcc.Dropdown(options = [{'label': key, 'value': key} for key in base.sets],
            style={'float':'left', 'width':'200px'}, id='del-sets-input',
            placeholder="Select a set", searchable=False),
        html.Button(id='submit-del-sets', n_clicks=0, children='Delete Sets', style={'float':'right'})],
        style={'height':'40px'}),
    html.Div(id='sets-result', style={'height':'32px'})]

Stocks = [
    html.H6("Select Stock"),
    dcc.Dropdown(id='select-stock-input',
            options = [],
            placeholder="Select stocks", searchable=False, multi=True),
    html.H6("New Stock", id='new-stock-name'),
    html.Div([
        dcc.Input(value='Stock Name/ID', id='new-stock-input', style={'float':'left'}, list='list-suggested-inputs'),
        html.Button(id='submit-new-stock', n_clicks=0, children='Create Stock', style={'float':'right'}, disabled=True)],
        style={'height':'32px'}),
    html.Datalist(id='list-suggested-inputs'),
    html.H6("Delete Stock", id='del-stock-name'),
    html.Div([
        dcc.Dropdown(options = [],
            style={'float':'left', 'width':'200px'}, id='del-stock-input',
            placeholder="Select a set", searchable=False),
        html.Button(id='submit-del-stock', n_clicks=0, children='Delete Stock', style={'float':'right'}, disabled=True)
        ],style={'height':'40px'}),
    html.Div("Stock Result", id='stock-result')]
        

head = html.Div([html.H1("Stocker Chung"), html.Div("Stock assitance tool for Chao-Tung Chung")],
                style={'text-align':'center', 'height':'100px','width':'950px','border-bottom': 'double','margin': '0 auto'})


SelectStocks = html.Div([
                html.Div(Sets, style={"width": '450px','height':'300px','float':'left'}),
                html.Div(Stocks, style={"width": "450px",'height':'300px','float':'right'}),],
                style={'columnCount': 1, 'width':'950px', 'margin': '0 auto','border-bottom': 'double'})


weekday_options = [
            {'label': 'All', 'value': 'all'},
            {'label': 'Mon', 'value': 'Monday', 'disabled':True},
            {'label': 'Tue', 'value': 'Tuesday', 'disabled':True},
            {'label': 'Wed', 'value': 'Wednesday', 'disabled':True},
            {'label': 'Thur', 'value': 'Thursday', 'disabled':True},
            {'label': 'Fri', 'value': 'Friday', 'disabled':True},
        ]
month_options = [
            {'label': 'All', 'value': 'all'},
            {'label': 'Jan', 'value': 1, 'disabled':True},
            {'label': 'Feb', 'value': 2, 'disabled':True},
            {'label': 'Mar', 'value': 3, 'disabled':True},
            {'label': 'Apl', 'value': 4, 'disabled':True},
            {'label': 'May', 'value': 5, 'disabled':True},
            {'label': 'Jun', 'value': 6, 'disabled':True},
            {'label': 'Jul', 'value': 7, 'disabled':True},
            {'label': 'Aug', 'value': 8, 'disabled':True},
            {'label': 'Set', 'value': 9, 'disabled':True},
            {'label': 'Oct', 'value': 10, 'disabled':True},
            {'label': 'Nov', 'value': 11, 'disabled':True},
            {'label': 'Dec', 'value': 12, 'disabled':True},
        ]

DataFilter = html.Div([
    html.Div([
        html.Label('Weekdays'),
        dcc.Checklist(id='weekday-filter',
            options=list([
                {'label': 'All', 'value': 'all'},
            ]),
            value=['all'],
            labelStyle={'display': 'inline-block'})],
        style = {'float':'left','width':'400px', 'height':'65px'}),
    html.Div([
        html.Label('Date Range'),
        dcc.DatePickerRange(id='date-range-filter',
            with_portal=True,
            end_date= datetime.date(today.year, today.month, today.day),
            start_date=datetime.date(2010,1,1),
            display_format='Y-M-D',
            start_date_placeholder_text='MM-DD-Y-Q'
            )],
        style = {'float':'right','width':'300px','height':'65px'}
        ),
    html.Div([
        html.Label('Month'),
        dcc.Checklist(id='month-filter',
            options=list([
                {'label': 'All', 'value': 'all'},
            ]),
            value=['all'],
            labelStyle={'display': 'inline-block'}),
        ],
        style = {'float':'left','width':'580px', 'height':'65px'})],
    style={'width':'950px', 'height':'130px','margin': '0 auto','border-bottom': 'double'})

col = ['Date','No','Open', 'Close', 'High', 'Low', 'Margin buy', 'Margin sell', 'Short buy', 'Short sell', 'Total net add', 'Rate']

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}




Plots = html.Div(
     dcc.Tabs(id="tabs-styled-with-inline", value='OV', children=[
        dcc.Tab(label='Overview', value='OV', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Probability Density', value='PDF', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Linear Regression', value='LG', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    style={'width':'950px', 'height':'600px','margin': '0 auto','border-bottom': 'double'})


DataTable = html.Div([dash_table.DataTable(
    id='datatable',
    columns=[{"name": i, "id": i} for i in col],
    page_size=30,
    filter_action="native",
    sort_action="native",
    fixed_columns={'headers':True},
    style_cell={
        'whiteSpace': 'normal',
        'height': 'auto',
        'textAlign': 'left'
    },
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
)], style={'width':'950px', 'height':'320px','margin': '0 auto','border-bottom': 'double'})


@app.callback(Output('weekday-filter', 'options'), Input('weekday-filter', 'value'))
def Select_weekday(weekdays):
    options = weekday_options
    if 'all' in weekdays:
        for i in range(1,6):
            options[i]['disabled'] = True
    else:
        for i in range(1,6):
            options[i]['disabled'] = False
    return options

@app.callback(Output('month-filter', 'options'), Input('month-filter', 'value'))
def Select_month(months):
    options = month_options
    if 'all' in months:
        for i in range(1,13):
            options[i]['disabled'] = True
    else:
        for i in range(1,13):
            options[i]['disabled'] = False
    return options


@app.callback(Output('datatable','data'), 
              Input('weekday-filter', 'value'),
              Input('month-filter', 'value'),
              Input('date-range-filter','start_date'),
              Input('date-range-filter','end_date'),
              Input('select-stock-input', 'value'))
def datafilter(limit_weekday, limit_month, min_date, max_date, stocks):   
    if stocks != None and len(stocks) > 0:
        stocks = [stock.split(' ')[1][1:-1] for stock in stocks if stock.find(" ")!=-1]
    else:
        return None
    output = list()
    for stock in stocks:
        df = base.stock_df[stock]
        df['Date'] = df.index
        df = df.loc[(df['Date']<max_date) & (df['Date']>min_date)]
        if 'all' not in limit_weekday and len(limit_weekday) > 0:
            mask1 = [day in limit_weekday for day in df['weekday']]
            df = df.loc[mask1]
        if 'all' not in limit_month and len(limit_month) > 0:
            mask2 = [month in limit_month for month in df['month']]
            df = df.loc[mask2]
        df['No'] = [stock]*len(df)
        col = ['Date','No','Open', 'Close', 'High', 'Low', 'Margin buy', 'Margin sell', 'Short buy', 'Short sell', 'Total net add', 'Rate']
        df = df.filter(col)
        df["Rate"] = (100 * df['Rate']).round(2)
        output.append(df)
    df = pd.concat(output)
    return df.to_dict('records')
        


@app.callback([Output('sets-result', 'children'),
               Output('new-sets-input','value'),
               Output('select-sets-input','options'),
               Output('del-sets-input','options')], 
              Input('submit-new-sets', 'n_clicks'), 
              Input('submit-del-sets', 'n_clicks'), 
              State('new-sets-input','value'),
              State('del-sets-input','value'))
def ChangeSets(bt1, bt2, NewName, DelName):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    word = "Ready"
    if 'submit-new-sets' in changed_id:
        if NewName in base.sets:
            word = NewName + " already exist."
        elif len(NewName) == 0:
            word = "Name can not be empty."
        else:
            base.NewSets(NewName)
            word = "Create Sets: " + NewName
    elif 'submit-del-sets' in changed_id:
        if DelName in base.sets:
            base.DeletSets(DelName)
            word = "Delete Sets: " + DelName
        else:
            word = "Please select a set to delete."
    options = [{'label':key, 'value':key} for key in base.sets]
    return [word, "", options, options]

@app.callback(Output('list-suggested-inputs','children'), Input('new-stock-input', 'value'))
def Set_Suggest(string):
    if len(string) == 0:
        return list()
    stocks = JsonStockData.GetStockInfo(string=string, Single=False)
    return [html.Option(value=word) for word in stocks]
     
@app.callback([Output('submit-new-stock','disabled'),
               Output('submit-del-stock','disabled'),
               Output('select-stock-input','options'),
               Output('del-stock-input','options'),
               Output('stock-result', 'children'),
               Output('new-stock-input','value')], 
              Input('select-sets-input','value'),
              Input('submit-new-stock', 'n_clicks'), 
              Input('submit-del-stock', 'n_clicks'), 
              State('new-stock-input','value'),
              State('del-stock-input','value'))
def SetSelected(set_name, btn1, btn2, NewName, DelName):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    options = list()
    if 'select-sets-input' in changed_id:
        if set_name in base.sets:
            stocks = base.sets[set_name]
            options = [{'label': key, 'value': key} for key in stocks]
            return [False, False, options, options, "", ""]
        else:
            return [True, True, list(), list(), "", ""] 

    word = ""
    if set_name in base.sets:
        if 'submit-new-stock' in changed_id:
            if NewName in base.sets[set_name]:
                word = NewName + " already exsit."
            elif len(NewName) == 0:
                word = "Name can not be empty."
            else:
                base.Set_add_Stock(sets=set_name, stock=NewName)
                word =  "Create Stock: " + NewName
        elif 'submit-del-stock' in changed_id:
            if DelName in base.sets[set_name]:
                base.Set_del_Stock(sets=set_name, stock=DelName)
                word = "Delete Stock: " + DelName
            else:
                word = "Not found " + DelName +"."
        if set_name in base.sets:
            options = [{'label':key, 'value':key} for key in base.sets[set_name]]
    return [False, False, options, options, word, ""]

app.layout = html.Div([head, SelectStocks, DataFilter, Plots, DataTable])
if __name__ == '__main__':
    app.run_server(debug=True)

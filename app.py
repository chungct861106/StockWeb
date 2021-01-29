import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import datetime
import JsonStockData
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

base = JsonStockData.JsonStockData()

current_df = None

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



Overview = html.Div([
    html.H3("Choose Stock"),
    dcc.Dropdown(id='overview-select', options = [{'label':JsonStockData.GetStockInfo(key, Single=True),
                                                   'value':key} for key in base.stock_df]),
    dcc.Graph(id='overview-plot')]
    )
@app.callback(Output('overview-plot', 'figure'),
              Input('overview-select','value'))
def OverViewPlot(stock):
    if not stock:
        return go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    stocks = base.stock_df[stock]
    stocks["Color"] = np.where(stocks["Close"]-stocks['Open']>0, 'red', 'green')
    Candlestick = go.Candlestick(x = stocks.index, open = stocks['Open'], 
                                 high = stocks['High'], low = stocks['Low'], 
                                 close = stocks['Close'], name='Stock Price',
                                 increasing_line_color= 'red', decreasing_line_color= 'green')
    Bar = go.Bar(x= stocks.index, y=abs(stocks['Close']-stocks['Open']), marker_color=stocks['Color'], name='Stock Growth')
    fig.add_trace(Candlestick,secondary_y=True)
    fig.add_trace(Bar,secondary_y=False)
    fig.update_layout(
        yaxis=dict(
            range = [0,max(stocks['Open']/10)],
            title="Growth",
            titlefont=dict(
            color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            range = [0,max(stocks['High'])],
            title="Stock Price",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            )))
    fig.update_yaxes(title_text = 'Price(NTD)', tickprefix = '$')
    return fig


col_obj = ['Margin buy', 'Margin sell', 'Short buy', 'Short sell', 'Total net add', 'Rate']
col_options = [{'label':key, 'value': key} for key in col_obj]
PDFs = html.Div([
    html.H3("Choose Probabilibty Desity Object"),
    dcc.Dropdown(id='PDF-object-input', options=col_options, value='Rate'),
    html.Div(id='PDF-result'),
    dcc.Graph(id='PDF-plot')])
@app.callback([Output('PDF-plot', 'figure'), Output('PDF-result','children')], 
              Input('datatable', 'derived_virtual_row_ids'),
              Input('PDF-object-input','value'))
def PDF_plot(row_ids, obj):
    current_df = base.current_df
    if len(current_df) == 0:
        return [go.Figure(),""]
    if row_ids is None:
        dff = current_df
        row_ids = dff['id']
    else:
        dff = current_df.loc[row_ids] 
    x = dff[obj]
    word = "Mean: %.2f    | Std: %.2f" % (x.mean(), x.std())
    fig = make_subplots(rows=2, cols=1)
    fig.append_trace(go.Histogram(x=x, histnorm='probability', name='PDF'), 1, 1)
    fig.append_trace(go.Histogram(x=x, histnorm='probability', cumulative_enabled=True, name='CDF'), 2, 1)
    return [fig, word]


LGcol = ['Open', 'Close', 'High', 'Low','Rate',
    'Margin buy','Margin sell','Margin used ratio',
    'Short buy','Short sell','Margin short ratio',
    'Dealer net add','Domestic net add','Foreign net add',
    'Total net add']
LG_options = [{'label': key, 'value':key} for key in LGcol]
Linear = html.Div([
    html.H3("Choose Comparison Objects"),
    dcc.Dropdown(id='LG-obj', options=LG_options, multi=True, value=['Total net add', 'Rate']),
    dcc.Graph(id='LG-plot')
    ])
@app.callback(Output('LG-plot', 'figure'), 
              Input('datatable', 'derived_virtual_row_ids'),
              Input('LG-obj','value'))
def LG_plot(row_ids, obj):
    current_df = base.current_df
    if len(current_df) == 0:
        return go.Figure()
    fig = px.scatter_matrix(current_df, dimensions=obj, color="No")
    return fig


Plots = html.Div(
     dcc.Tabs(id="tabs-styled-with-inline", value='OV', children=[
        dcc.Tab(label='Overview', value='OV', style=tab_style, selected_style=tab_selected_style, children=[Overview]),
        dcc.Tab(label='Probability Density', value='PDF', style=tab_style, selected_style=tab_selected_style, children=[PDFs]),
        dcc.Tab(label='Linear Regression', value='LG', style=tab_style, selected_style=tab_selected_style, children=[Linear])
    ], style=tabs_styles),
    style={'width':'950px', 'height':'600px','margin': '0 auto','border-bottom': 'double'})

col = ['Date','No','Open', 'Close', 'High', 'Low', 'Rate',
                'Margin buy','Margin sell','Margin used ratio',
                'Short buy','Short sell','Margin short ratio',
                'Dealer net add','Domestic net add','Foreign net add',
                'Total net add']

DataTable = html.Div([dash_table.DataTable(
    id='datatable',
    columns=[{"name": i, "id": i} for i in col],
    page_size=30,
    filter_action="native",
    sort_action="native",
    fixed_columns={'headers':True},
    style_cell={'textAlign': 'left'},
    style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
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
        col = ['Date','No','Open', 'Close', 'High', 'Low', 'Rate',
                'Margin buy','Margin sell','Margin used ratio',
                'Short buy','Short sell','Margin short ratio',
                'Dealer net add','Domestic net add','Foreign net add',
                'Total net add']
        df = df.filter(col)
        df["Rate"] = (100 * df['Rate']).round(2)
        output.append(df)
    df = pd.concat(output)
    df.index = range(len(df))
    df['id'] = df.index
    base.current_df = df
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

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import JsonStockData

base = JsonStockData.JsonStockData()
current_options = []

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

suggestions = []



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
    html.Datalist(
        id='list-suggested-inputs', 
        children=[html.Option(value=word) for word in suggestions]),
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

Overview = dcc.Graph()

weekday_options = [
            {'label': 'All', 'value': 'all'},
            {'label': 'Mon', 'value': 'Monday', 'disabled':True},
            {'label': 'Tue', 'value': 'Tuesday', 'disabled':True},
            {'label': 'Wed', 'value': 'Wednesday', 'disabled':True},
            {'label': 'Thur', 'value': 'Thursday', 'disabled':True},
            {'label': 'Fri', 'value': 'Friday', 'disabled':True},
            {'label': 'Sat', 'value': 'Saturday', 'disabled':True},
            {'label': 'Sun', 'value': 'Sunday', 'disabled':True},
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
    html.Label('Weekdays'),
    dcc.Checklist(id='weekday-filter',
        options=list([
            {'label': 'All', 'value': 'all'},
        ]),
        value=['all'],
        labelStyle={'display': 'inline-block'},
        style = {'width':'400px'}),
    html.Label('Month'),
    dcc.Checklist(id='month-filter',
        options=list([
            {'label': 'All', 'value': 'all'},
        ]),
        value=['all'],
        labelStyle={'display': 'inline-block'},
        style = {'width':'380px'}),
    ],
    style={'columnCount': 1, 'width':'950px', 'margin': '0 auto','border-bottom': 'double'})
@app.callback(Output('weekday-filter', 'options'), Input('weekday-filter', 'value'))
def Select_weekday(weekdays):
    options = weekday_options
    if 'all' in weekdays:
        for i in range(1,8):
            options[i]['disabled'] = True
    else:
        for i in range(1,8):
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

        
    
        
# Tabs = html.Div([
#      dcc.Tabs(id='tabs-example', value='tab-1', children=[
#         dcc.Tab(label='Tab one', children=[
#             dcc.Graph(
#                 figure={
#                     'data': [
#                         {'x': [1, 2, 3], 'y': [4, 1, 2],
#                             'type': 'bar', 'name': 'SF'},
#                         {'x': [1, 2, 3], 'y': [2, 4, 5],
#                          'type': 'bar', 'name': u'Montréal'},
#                     ]
#                 }
#             )
#         ]),
#         dcc.Tab(label='Tab two', children=[
#             dcc.Graph(
#                 figure={
#                     'data': [
#                         {'x': [1, 2, 3], 'y': [1, 4, 1],
#                             'type': 'bar', 'name': 'SF'},
#                         {'x': [1, 2, 3], 'y': [1, 2, 3],
#                          'type': 'bar', 'name': u'Montréal'},
#                     ]
#                 }
#             )
#         ]),
#         dcc.Tab(label='Tab three', children=[
#             dcc.Graph(
#                 figure={JsonStockData.test_plot()}
#             )
#         ])
#     ])],
#     style={'text-align':'center',
#            'height':'600px','width':'950px',
#            'border-bottom': 'double',
#            'border-right': 'double',
#            'border-left':'double',
#            'margin': '0 auto'}
#     )

app.layout = html.Div([head, SelectStocks, DataFilter])


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


if __name__ == '__main__':
    app.run_server(debug=True)

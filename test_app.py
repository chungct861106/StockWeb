import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import JsonStockData

base = JsonStockData.JsonStockData()
current_options = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
food_names_arr = ['banana','apple','strawberry','blueberrys','pineapple','watermelon','orange']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        dcc.Input(
            id="search_ingredient", type="search",
            autoComplete='on',
            list="food_names", placeholder=food_names_arr[0]
        ),
        html.Datalist(
            id="food_names", children=[
                html.Option(value=food) for food in food_names_arr
    ]
)

    ])



    
if __name__ == '__main__':
    app.run_server(debug=True)
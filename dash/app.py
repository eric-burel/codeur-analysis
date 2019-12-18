# -*- coding: utf-8 -*-
import psycopg2.extras
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
import json
import atexit
from os import sys
import pandas as pd
import utils

# Connect to the db
import psycopg2
connection = None

try:
    connection = psycopg2.connect(user="postgres",
                                  password="admin123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")
    cursor = connection.cursor()
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    cursor.close()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
    sys.exit()


def close_connection():
    # closing database connection.
    if(connection):
        connection.close()
        print("PostgreSQL connection is closed")


atexit.register(close_connection)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def search_to_sql_like(search_terms):
    return search_terms.split(',')


MAX_DATE = datetime.now().year
MIN_DATE = 2016

DEFAULT_DATA = [
    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
]

app.layout = html.Div(children=[
    html.H1(children='Codeur.com analysis'),

    # html.Div(children='''
    #    Dash: A web application framework for Python.
    # '''),
    dcc.Input(
        id="search-terms",
        placeholder="search..."
    ),
    html.Div(
        id="results-summary"
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=MIN_DATE,  # df['year'].min(),
        max=MAX_DATE,  # df['year'].max(),
        value=[MIN_DATE, MAX_DATE],
        marks={str(year): str(year)
               for year in range(MIN_DATE, MAX_DATE+1, 1)},
        step=None
    ),
    # Date picker version (eg for more precise find)
    # dcc.DatePickerRange(
    #    id='year-slider',
    #    min_date_allowed=datetime(MIN_DATE, 1, 1),  # df['year'].min(),
    #    max_date_allowed=datetime(MAX_DATE, 12, 1),  # df['year'].max(),
    #    start_date=datetime(MIN_DATE, 1, 1),  # df['year'].min(),
    #    end_date=datetime(MAX_DATE, 12, 1),  # df['year'].max(),
    # ),
    dcc.Graph(
        id="yearly-graph",
        figure={
            'data': DEFAULT_DATA,
            'layout': {
                'title': 'Project count per month'
            }
        }
    ),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='query-results', style={'display': 'none'})
])


# SQL Query + intermediate storage of result depending on inputs
@app.callback(
    Output(component_id='query-results', component_property='children'),
    [Input(component_id='search-terms', component_property='value'),
     Input(component_id='year-slider', component_property='value')]
)
def update_output_div(input_value, years):
    if input_value is None:
        return None

    start_year, end_year = years

    query = """
    SELECT
    id, title, published_at
    from scraper_codeurproject
    where title ilike %(ilike)s
    or description ilike %(ilike)s
    and published_at >= %(start_year)s
    and published_at <= %(end_year)s
    """
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Print PostgreSQL version
    cursor.execute(query, {
        "ilike": "%{}%".format(input_value),
        "start_year": "{}-01-01".format(start_year),
        "end_year": "{}-12-31".format(end_year)
    })
    res = cursor.fetchall()
    # 'You\'ve entered "{}"'.format(input_value)
    return json.dumps({
        "data": res,
        "count": len(res),
        "start_year": start_year,
        "end_year": end_year,
        "terms": input_value
    },
        # default parser (eg for datetime)
        default=str)


@app.callback(
    Output(component_id='results-summary', component_property="children"),
    [Input(component_id="query-results", component_property="children")]
)
def update_query_summary(results_dump):
    if results_dump is None:
        return None
    results = json.loads(results_dump)
    #data = results["data"]
    count = results["count"]
    start_year = results["start_year"]
    end_year = results["end_year"]
    terms = results["terms"]
    return 'Found {} projects for years {} to {} and search terms {}'.format(count, start_year, end_year, terms)


# Update history graph
@app.callback(
    Output(component_id="yearly-graph", component_property="figure"),
    [Input(component_id='query-results', component_property="children")]
)
def update_graph(results_dump):
    if results_dump is None:
        return {"data": DEFAULT_DATA}
    results = json.loads(results_dump)
    # compute ticks
    start_year = results["start_year"]
    end_year = results["end_year"]
    all_x = [(year, month)
             for year in range(start_year, end_year + 1)
             for month in range(1, 12 + 1)
             ]
    # compute values
    # as map so we add zeros where they miss (todo: could be done with pandas probably)
    data = results["data"]
    if (len(data)):
        df = pd.DataFrame(data)
        utils.split_date(df)
        df_per_month = utils.per_month(df)
        per_month_count = utils.count(df_per_month)
        y_map = {
            year_month: per_month_count["count"].loc[year_month]
            for year_month in per_month_count.index
        }
    else:
        # no data
        y_map = {}

    y = [
        y_map[year_month] if year_month in y_map else 0
        for year_month in all_x
    ]
    # TODO: whats the correct value?
    x = ["{}-{}-01".format(year, month)
         for (year, month) in all_x]  # list(range(0, len(y)))
    return {
        "data": [{
            "x": x,
            "y": y,
            "type": "bar",
        }],
        "layout": {
            "xaxis": {
                "tickformat": "%Y/%m"
            }
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)

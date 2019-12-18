# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
import json
import atexit
from os import sys

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
    dcc.Slider(
        id='year-slider',
        min=MIN_DATE,  # df['year'].min(),
        max=MAX_DATE,  # df['year'].max(),
        value=MIN_DATE,
        marks={str(year): str(year)
               for year in range(MIN_DATE, MAX_DATE+1, 1)},
        step=None
    ),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5],
                    'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
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
def update_output_div(input_value, year):
    if input_value is None:
        return None

    query = """
    SELECT
    id, title, published_at
    from scraper_codeurproject
    where title ilike %(ilike)s
    or description ilike %(ilike)s
    and published_at >= %(start_year)s
    and published_at <= %(end_year)s
    """
    cursor = connection.cursor()
    # Print PostgreSQL version
    cursor.execute(query, {
        "ilike": "%{}%".format(input_value),
        "start_year": "{}-01-01".format(year),
        "end_year": "{}-12-31".format(year)
    })
    res = cursor.fetchall()
    # 'You\'ve entered "{}"'.format(input_value)
    return json.dumps({
        "data": res,
        "count": len(res),
        "year": year,
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
    year = results["year"]
    terms = results["terms"]
    return 'Found {} projects for year {} and search terms {}'.format(count, year, terms)


if __name__ == '__main__':
    app.run_server(debug=True)

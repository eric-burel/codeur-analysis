# -*- coding: utf-8 -*-
import psycopg2.extras
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from datetime import datetime
import json
import os
from os import sys
import pandas as pd
import utils
from figures import empty_figure
from db import connect
import dash_auth
import dash_standard_button as dsb

USERS = json.loads(
    os.environ.get('USERS_BASIC_DUMP',
                   json.dumps([
                       ("admin", "admin")
                   ]))
)

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dash_auth.BasicAuth(
    app,
    USERS
)


# db connection
connection = connect()


def search_to_sql_like(search_terms):
    return search_terms.split(',')


MAX_DATE = datetime.now().year
MIN_DATE = 2016

DEFAULT_DATA = [
    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
]


app.layout = html.Section(
    className="section",
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="level",
                    children=[
                        html.H1(className="title",
                                children='Codeur.com analysis'),
                        dsb.StandardButton(
                            className="button is-small logout-button",
                            onClick="logout();",
                            children="Logout"
                        ),

                    ]
                ),
                html.Div(className="columns", children=[
                    html.Div(className="column is-half-desktop", children=[
                        html.Label(
                            className="label",
                            children="Keywords:"
                        ),
                        dcc.Input(
                            className="input",
                            id="search-terms",
                            placeholder="search..."
                        ),
                    ]),
                    html.Div(className="column is-half-desktop", children=[
                        html.Label(
                            className="label",
                            children="Period:"
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
                    ]),
                ]),
                html.P(
                    id="results-summary"
                ),
            ]),
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
            figure=empty_figure("Type a keyword to view projects history")
            # figure={
            #    'data': DEFAULT_DATA,
            #    'layout': {
            #        'title': 'Project count per month'
            #    }
            # }
        ),
        # dcc.Graph(id="empty", figure=empty_figure("hello")),
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
    # Update condition
    if input_value is None:
        raise PreventUpdate

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
    # Update conditions
    if results_dump is None:
        raise PreventUpdate
    results = json.loads(results_dump)
    # data = results["data"]
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
    # Update conditions
    if results_dump is None:
        raise PreventUpdate
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

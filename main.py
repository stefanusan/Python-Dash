import numpy
from sqlalchemy import create_engine
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import dash_table

import plotly.graph_objects as go


user = "root"
password = ""
host = "localhost"
port = 3306
database = "python_dash"

connect = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
YT_LOGO = "https://assets.stickpng.com/images/580b57fcd9996e24bc43c545.png"

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#edffec",
    "zIndex": "1"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "15rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}
# background
control = dbc.FormGroup(
    [
        html.P('LED & LKPS', style={
            'textAlign': 'left'
        }),

    ]
)

sidebar = html.Div(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=YT_LOGO, height="30px")),
                    # dbc.Col(dbc.NavbarBrand("STEFA", className="ml-2", style={'color': 'black', 'height':'100%'})),
                ],
                align="left",
                no_gutters=True,
            ),
            href="https://www.youtube.com/watch?v=qZ6T4bMi93M",
        ),
        html.Hr(),
        html.H2("STEFA", className="display-4"),
        html.Hr(),
        html.P(
            "Information", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("Detail Info", href="/detailinfo", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

navbar = dbc.Navbar(
    id="navbar",
    style={"position": "fixed", "width": "100%", "zIndex": "1", 'margin': '0px 0px 0px 0px'},
    color="#edffec",
    dark=True,
)

#page
content = html.Div(
    html.Div(id="page-content", style=CONTENT_STYLE)
)

#inti
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
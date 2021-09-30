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

#query
df_info = pd.read_sql("""SELECT * FROM us_500""", connect)

df_org_line = pd.read_sql("""SELECT COUNT(DISTINCT first_name) AS 'Jumlah', state AS 'State' FROM us_500 
                GROUP BY state ORDER BY state ASC""", connect)
fig_org_line = px.line(
    df_org_line,
    x=df_org_line["State"],
    y=df_org_line["Jumlah"]
)
fig_org_bar = px.bar(
    df_org_line,
    x=df_org_line["State"],
    y=df_org_line["Jumlah"]
)

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


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def render_page_content(pathname): \

    if pathname == "/":
        return \
            html.Div([
                html.H3("Visualisasi Data", className="display-6",
                        style={'textAlign': 'center', 'margin': '0px 0px 0px 0px'}),

                dbc.Card(className='card text-white bg-secondary mb-3', children=[
                    html.H4('Jumlah Orang',
                            style={'margin': '10px 10px 0px 20px', 'color': 'white', },
                            className='card-title'),

                    dbc.Row([
                        dbc.Col([
                            dbc.CardBody([
                                html.H6('"Grafik Bar"', className="card-title",
                                        style={'textAlign': 'center'}),
                                dcc.Graph(
                                    # id='graph-org-line',
                                    figure=fig_org_bar
                                ),
                            ])
                        ]),
                        dbc.Col([
                            dbc.CardBody([
                                html.H6('"Grafik Line"',
                                        className="card-title",
                                        style={'textAlign': 'center'}),
                                dcc.Graph(
                                    # id='graph-mhs-aktif-angkatan',
                                    figure=fig_org_line,
                                )
                            ])
                        ]),
                    ]),

                ]),

            ], style={'margin': '0px 0px 0px 0px'})

    elif pathname == "/detailinfo":
        return \
            html.Div([
                html.H3("Visualisasi Datatable", className="display-6",
                        style={'textAlign': 'center', 'margin': '0px 0px 0px 0px'}),

                dash_table.DataTable(
                    id='table-filtering-be',
                    columns=[
                        {"name": i, "id": i} for i in (df_info.columns)
                    ],

                    filter_action='custom',
                    filter_query=''
                ),

            ], style={'margin': '0px 0px 0px 0px'})

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], style={'margin': '100px 0px 0px 0px'}
    )

#=====datatable=====
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(
    Output('table-filtering-be', "data"),
    Input('table-filtering-be', "filter_query"))
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    df_table_dosenf = df_info
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            df_table_dosenf = df_table_dosenf.loc[getattr(df_table_dosenf[col_name], operator)(filter_value)]
        elif operator == 'contains':
            df_table_dosenf = df_table_dosenf.loc[df_table_dosenf[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            df_table_dosenf = df_table_dosenf.loc[df_table_dosenf[col_name].str.startswith(filter_value)]

    return df_table_dosenf.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)
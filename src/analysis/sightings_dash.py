"""
This script runs the dash website
that visualizes the Analysis of Sightings data
"""

import json
import os

import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import support_files.rule_mining_sequences as sequences
import support_files.technique_time_series as TS
from dash.dependencies import Input, Output

# ------ import support files
from support_files.barcharts_object import Barcharts

styles_json = open("support_files/sightings_dash_styles.json")

# ------ grab connection string from environment variable
sighting_db_conn_str = os.environ["sighting_db_conn_str"]

# ------ setup for barchart tiles
variables_list = ["detection_type", "sighting_type"]
barcharts = Barcharts(variables_list=variables_list, db_connection_string=sighting_db_conn_str)
barcharts.frequency_dist(cutoff=90)
# ------ setup for rule mining tile
G, stylesheet = sequences.get_graph(sighting_db_conn_str=sighting_db_conn_str)
title_seq, blurb_seq = sequences.get_verbage()
# ------ setup for time series tile
ts = TS.get_graph(sighting_db_conn_str=sighting_db_conn_str)
title_ts, blurb_ts = TS.get_verbage()
# ------ setup style-sheet
styles = json.load(styles_json)
# ---------------------------- start app
app = dash.Dash(__name__)
# ---------------------------- app layout which has all components
app.layout = html.Div(
    style=styles["body"],
    children=[
        html.Div(
            style=styles["pageHeader"],
            children=[html.H1("What Do the Sightings Tell Us?")],
        ),
        # ----- Start tile 1
        html.Br(),
        html.Div(
            style=styles["container"],
            children=[
                html.Div(
                    style=styles["verbage"],
                    children=[
                        html.H2(barcharts.title_barchart),
                        html.P(barcharts.blurb_barchart),
                    ],
                ),
                html.Div(
                    style=styles["grp"],
                    children=[
                        html.Div(
                            style={"width": "70%", "height": "100%"},
                            children=[
                                dcc.Graph(
                                    id="top_techniques",
                                    figure=barcharts.technique_barchart,
                                    config={"responsive": True},
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
        # ----- End tile 1
        # ----- Start tile 2
        html.Br(),
        html.Div(
            style=styles["container"],
            children=[
                html.Div(
                    style=styles["verbage"],
                    children=[html.H2(id="title_grouped"), html.P(id="blurb_grouped")],
                ),
                html.Div(
                    dcc.Dropdown(
                        id="dropdown",
                        options=[{"label": x, "value": x} for x in variables_list],
                        value=variables_list[0],
                    )
                ),
                html.Div(
                    style=styles["grp"],
                    children=[
                        html.Div(
                            style={"width": "70%", "height": "100%"},
                            children=[
                                dcc.Graph(
                                    id="top_techniques_grouped",
                                    config={"responsive": True},
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
        # ----- End tile 2
        # ----- Start tile 3
        html.Br(),
        html.Div(
            style=styles["container"],
            children=[
                html.Div(
                    style=styles["verbage"],
                    children=[html.H2(title_seq), html.P(blurb_seq)],
                ),
                html.Div(
                    style=styles["grp"],
                    children=[
                        html.Div(
                            children=[
                                cyto.Cytoscape(
                                    style={"width": "800px", "height": "800px"},
                                    responsive=True,
                                    id="technique_rules",
                                    elements=nx.readwrite.json_graph.cytoscape_data(G)["elements"],
                                    layout={
                                        "name": "cose",
                                        "nodeDimensionsIncludeLabels": "true",
                                    },
                                    stylesheet=stylesheet,
                                    minZoom=1,
                                    maxZoom=5,
                                )
                            ]
                        ),
                    ],
                ),
            ],
        ),
        # ----- End tile 3
        # ----- Start tile 4
        html.Br(),
        html.Div(
            style=styles["container"],
            children=[
                html.Div(
                    style=styles["verbage"],
                    children=[html.H2(title_ts), html.P(blurb_ts)],
                ),
                html.Div(
                    style=styles["grp"],
                    children=[
                        html.Div(
                            style={"width": "70%", "height": "100%"},
                            children=[
                                dcc.Graph(
                                    figure=ts,
                                    id="ts_techniques",
                                    config={"responsive": True},
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
        # ----- End tile 4
    ],
)
# -------------------Start Callback section


@app.callback(
    Output("top_techniques_grouped", "figure"),
    Output("title_grouped", "children"),
    Output("blurb_grouped", "children"),
    [Input("dropdown", "value")],
)
def update_grouped_barchart(variable_of_interest, barcharts=barcharts):
    barcharts.frequency_dist_grouped(variable_of_interest)
    return (
        barcharts.technique_barchart_grouped,
        barcharts.title_barchart_grouped,
        barcharts.blurb_barchart_grouped,
    )


# -------------------End Callback section
if __name__ == "__main__":  # pragma: no cover
    app.run_server(host="0.0.0.0", debug=False, port=8050)

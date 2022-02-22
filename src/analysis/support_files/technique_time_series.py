"""
Support script for interactive time series chart
of techniques used in dash website
"""

import pandas as pd
import plotly.express as px
import psycopg2


def get_graph(sighting_db_conn_str):
    connection = psycopg2.connect(sighting_db_conn_str)

    cursor = connection.cursor()
    cursor.execute(
        (
            "select date_trunc('month',start_time)"
            " as date_to_month, technique_id, count(*) as freq\n"
            "from public.flattened_sightings\n"
            "group by date_to_month, technique_id\n"
            "order by date_to_month asc;"
        )
    )

    technique_time = cursor.fetchall()
    technique_df = pd.DataFrame(technique_time, columns=["Month", "Technique", "freq"])
    cursor.close()
    connection.close()

    fig = px.line(
        technique_df, x="Month", y="freq", color="Technique", line_group="Technique", hover_name="Technique", height=800
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    return fig


def get_verbage():
    title = "How Does The Frequency Distribution Of Techniques Evolve Over Time"
    blurb = (
        "Explore Techniques' distributions over time"
        " using the line chart below.\n"
        "Most prevalent techniques are at the top of the legend.\n"
        "Double click on a technique in the legend to isolate its curve.\n"
        "To select the time-range, use the buttons or slider above"
        " and below the chart respectively."
    )
    return title, blurb

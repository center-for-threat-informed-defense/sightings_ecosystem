"""
Support script for rule mining analysis used in dash website
"""
import networkx as nx
import pandas as pd

# --------------------- Setup for DiGraph of techniques
import psycopg2
from helper_functions.rules_object import AssociativeRules


def get_graph(sighting_db_conn_str):
    connection = psycopg2.connect(sighting_db_conn_str)

    cursor = connection.cursor()
    cursor.execute("drop view if exists sequences; ")
    cursor.execute(
        (
            "CREATE VIEW sequences AS\n"
            "   SELECT sighting_pid, string_agg(technique_id,',')"
            " AS seq, count(*) AS len\n"
            "   FROM public.flattened_sightings\n"
            "   GROUP BY sighting_pid\n"
            "   ORDER BY len DESC;"
        )
    )
    # TODO should this query end with 'len>1' or 'len>=1'
    cursor.execute("select seq from sequences where len>=1;")
    technique_freqs = cursor.fetchall()

    df_sequence = pd.DataFrame(technique_freqs, columns=["sequence_string"], dtype="string")
    df_sequence["sequence_set"] = df_sequence["sequence_string"].apply(lambda x: set(x.split(",")))

    rules_sets = AssociativeRules(groups=df_sequence["sequence_set"], order=False, threshold=0.5, rule_filter="conf")
    rules_sets.find_assoc_rules()
    list_of_rules = rules_sets.list_of_rules

    df = pd.DataFrame(list_of_rules, columns=["source", "target", "conf"])
    # Graph
    G = nx.from_pandas_edgelist(df, source="source", target="target", edge_attr="conf", create_using=nx.DiGraph)

    stylesheet = [
        {
            "selector": "node",
            "css": {
                "content": "data(id)",
                "text-valign": "center",
                "color": "white",
                "text-outline-width": 2,
                "text-outline-color": "blue",
                "text-wrap": "wrap",
                "text-max-width": "10px",
                "text-overflow-wrap": "whitespace",
                "background-color": "blue",
            },
        },
        {
            "selector": "edge",
            "css": {"mid-target-arrow-shape": "triangle", "mid-target-arrow-fill": "filled", "arrow-scale": 1},
        },
    ]

    cursor.close()
    connection.close()
    return G, stylesheet


def get_verbage():
    title = "Which Techniques Occur Together?"
    blurb = (
        "Techniques are visualized as nodes of the network graph"
        " and Association Rule mining was used to find techniques"
        " that tend to co-occur. If technique-B tends to occur"
        " when technique-A occurs, n arrow is drawn from A to B."
    )
    return title, blurb

"""
Support script for interactive barcharts used in dash website
"""
import pandas as pd
import plotly.express as px
import psycopg2


class Barcharts:
    def __init__(self, variables_list, db_connection_string):
        self.cutoff = None
        self.variables_list = variables_list
        self.variables_string = ",".join(self.variables_list)
        self.variable_of_interest = None
        self.total = None
        self.technique_barchart = None
        self.technique_barchart_grouped = None
        self.title_barchart = None
        self.blurb_barchart = None
        self.title_barchart_grouped = None
        self.blurb_barchart_grouped = None
        self.db_connection_string = db_connection_string

    def frequency_dist(self, cutoff=80):

        connection = psycopg2.connect(self.db_connection_string)

        cursor = connection.cursor()

        self.cutoff = cutoff
        cursor.execute("select count (*) from public.flattened_sightings")
        self.total = float(cursor.fetchone()[0])

        cursor.execute(
            (
                "DROP VIEW IF EXISTS technique_freqs_view,"
                " technique_freqs_filtered_view, techniques_sightings_metadata;"
            )
        )
        query_technique_freqs = (
            "CREATE VIEW technique_freqs_view AS\n"
            "WITH data AS\n"
            "   (SELECT technique_id, COUNT(*) AS freq\n"
            "   FROM public.flattened_sightings\n"
            "   GROUP BY technique_id\n"
            "   ORDER BY freq DESC)\n"
            "SELECT technique_id, freq,"
            f" cast(100 * freq / {self.total} AS numeric(6,2))"
            " freq_percentage, cast(100 * sum(freq) over (order by"
            " freq desc rows between unbounded preceding and current row) /"
            f" {self.total} AS numeric(6,2)) cumulative_percentage\n"
            "FROM data;"
        )

        cursor.execute(query_technique_freqs)
        cursor.execute(
            f"""create view technique_freqs_filtered_view as
                       select * from technique_freqs_view
                       where cumulative_percentage < {cutoff}"""
        )
        cursor.execute(
            (
                "CREATE VIEW techniques_sightings_metadata AS\n"
                "SELECT public.flattened_sightings.technique_id,"
                f" {self.variables_string}\n"
                "FROM public.flattened_sightings INNER"
                " JOIN technique_freqs_filtered_view\n"
                "ON public.flattened_sightings.technique_id ="
                " technique_freqs_filtered_view.technique_id;"
            )
        )
        cursor.execute(
            (
                "SELECT technique_id, freq, freq_percentage,"
                " cumulative_percentage\n"
                "FROM technique_freqs_filtered_view;"
            )
        )
        technique_freq = cursor.fetchall()
        technique_df = pd.DataFrame(
            technique_freq, columns=["Technique", "freq", "freq_percentage", "cumulative_percent"]
        )
        fig1 = px.bar(
            technique_df,
            x="freq_percentage",
            y="Technique",
            labels={"Technique": "Technique", "freq_percentage": "Percent", "cumulative_percent": "Cumulative Percent"},
            title="Top Techniques",
            height=800,
            orientation="h",
            hover_data={"Technique": True, "freq_percentage": True, "cumulative_percent": False},
        )
        fig1.layout.autosize = True
        fig1.update_yaxes(categoryorder="total ascending")
        self.technique_barchart = fig1
        self.title_barchart = "What Are the Top Techniques Seen in Sightings?"
        self.blurb_barchart = f"""These Techniques make up {self.cutoff}% of Sightings
        and their percentage contributions are shown."""

        connection.commit()
        cursor.close()
        connection.close()

    def frequency_dist_grouped(self, variable_of_interest):
        connection = psycopg2.connect(self.db_connection_string)

        cursor = connection.cursor()

        self.variable_of_interest = variable_of_interest

        cursor.execute(
            f"""
            with data as
                (select technique_id, {variable_of_interest}, count(*) as freq
                from techniques_sightings_metadata
                group by technique_id, {variable_of_interest}
                order by freq desc)

                select technique_id, {variable_of_interest}, freq,
                    cast(100 *
                            freq/
                            {self.total} AS numeric(6,2)) freq_percentage
                    from data;
        """
        )
        technique_grouped_freq = cursor.fetchall()

        df_grouped = pd.DataFrame(
            technique_grouped_freq, columns=["techniques", variable_of_interest, "freq", "freq_percentage"]
        )

        fig2 = px.bar(
            df_grouped,
            x="freq_percentage",
            y="techniques",
            labels={"techniques": "Technique", "freq_percentage": "Percent"},
            title=f"Top Techniques by {variable_of_interest}",
            color=f"{variable_of_interest}",
            height=800,
            orientation="h",
        )
        fig2.layout.autosize = True
        fig2.update_yaxes(categoryorder="total ascending")

        self.technique_barchart_grouped = fig2
        self.title_barchart_grouped = "How are the Top Techniques divided" " by a given variable of interest?"
        self.blurb_barchart_grouped = (
            f"These Techniques again make up {self.cutoff}% of Sightings"
            " and their percentage contributions"
            f" by {self.variable_of_interest} are shown."
            "Please toggle to your variable of interest:"
        )

        cursor.close()
        connection.close()

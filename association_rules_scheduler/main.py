import os
import sys
import pandas as pd
import json
import tempfile
from mlxtend.frequent_patterns import apriori, association_rules

sys.path.insert(0, os.getcwd())
from helper_functions.db_connection import (
    return_evidence_log,
)
from helper_functions.data_cleaning_functions import (
    add_base_article_slug_to_df,
    reduce_df_one_transaction_per_user,
    reduce_df_to_users_with_more_than_n_articles_read,
    return_df_for_apriori,
)

from google.cloud import bigquery


"""
Run this command within this folder after being logged in GCP to deploy the cloud function
gcloud functions deploy association_rules_scheduler --region=europe-west1 --entry-point main --runtime python39 --trigger-resource association_rules --trigger-event google.pubsub.topic.publish --timeout 540s --memory 1024MB
"""

"""
Environment variables
1. min_number_of_articles_read = the minimum of articles a user must have read to be used for the analysis
2. min_support = minimum required support for the itemsets
3. min_confidence = minimum required confidence for the itemsets
"""
MIN_NUMBER_OF_ARTICLES_READ = 8
MIN_SUPPORT = 0.05
MIN_CONFIDENCE = 0.5

tmpdir = tempfile.gettempdir()
_dir = os.path.dirname(__file__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _dir + "/bigquery_credentials.json"

association_rules_table_id = "bigquery_project_id.analytics.association_rules"
association_rules_lookup_table_id = "bigquery_project_id.analytics.association_rules_lookup"

# Load schema for association rules table
rules_schema_file = open(_dir + "/rules_schema.json")
rules_schema = json.load(rules_schema_file)

# Load schema for association rules lookup table
rules_lookup_schema_file = open(_dir + "/rules_lookup_schema.json")
rules_lookup_schema = json.load(rules_lookup_schema_file)


def clean_bigquery(client, bigquery_table_id):
    # Clean bigquery table
    query = f"""DELETE FROM `{bigquery_table_id}` WHERE true;"""
    query_job = client.query(query)
    return query_job.result()


def upload_to_bigquery(client, bigquery_table_id, json_schema, file_path_csv):
    # Upload rules to bigquery
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        schema=json_schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    with open(file_path_csv, "rb") as source_file:
        job = client.load_table_from_file(
            source_file, bigquery_table_id, job_config=job_config
        )

    return job.result()


def main(data, context):
    # Prepare evidencelog for the apriori analysis
    evidence_log_df = return_evidence_log()
    evidence_log_df = add_base_article_slug_to_df(evidence_log_df)
    evidence_log_df = reduce_df_one_transaction_per_user(evidence_log_df)
    evidence_log_df = reduce_df_to_users_with_more_than_n_articles_read(
        evidence_log_df, min_number_of_articles_read=MIN_NUMBER_OF_ARTICLES_READ
    )
    apriori_df = return_df_for_apriori(evidence_log_df)

    # Perform apriori analysis
    freq_items_df = apriori(apriori_df, min_support=MIN_SUPPORT, use_colnames=True)
    rules_df = association_rules(
        freq_items_df, metric="confidence", min_threshold=MIN_CONFIDENCE
    )
    # Convert antecedents and consequents into strings
    rules_df["antecedents"] = rules_df["antecedents"].astype(str).str[12:-3]
    rules_df["consequents"] = rules_df["consequents"].astype(str).str[12:-3]
    rules_df = rules_df.rename(
        columns={
            "antecedent support": "antecedent_support",
            "consequent support": "consequent_support",
        }
    )

    file_path_rules_csv = tmpdir + "/association_rules.csv"
    rules_df.to_csv(file_path_rules_csv, index=False)

    rules_for_lookup_df = (
        rules_df[["antecedents", "consequents"]]
        .set_index(["antecedents"])
        .apply(lambda x: x.str.split(", ").explode())
        .reset_index()
    )

    rules_for_lookup_df = (
        rules_for_lookup_df[["antecedents", "consequents"]]
        .set_index(["consequents"])
        .apply(lambda x: x.str.split(", ").explode())
        .reset_index()
    )

    rules_for_lookup_df['antecedents'] = rules_for_lookup_df['antecedents'].str.replace("'","")
    rules_for_lookup_df['consequents'] = rules_for_lookup_df['consequents'].str.replace("'","")

    rules_for_lookup_df = rules_for_lookup_df.drop_duplicates()

    file_path_rules_lookup_csv = tmpdir + "/association_rules_lookup.csv"
    rules_for_lookup_df.to_csv(file_path_rules_lookup_csv, index=False)

    client = bigquery.Client()
    clean_bigquery(client, association_rules_table_id)
    upload_to_bigquery(
        client=client,
        bigquery_table_id=association_rules_table_id,
        json_schema=rules_schema,
        file_path_csv=file_path_rules_csv,
    )

    clean_bigquery(client, association_rules_lookup_table_id)
    upload_to_bigquery(
        client=client,
        bigquery_table_id=association_rules_lookup_table_id,
        json_schema=rules_lookup_schema,
        file_path_csv=file_path_rules_lookup_csv,
    )


if __name__ == "__main__":
    main("data", "context")

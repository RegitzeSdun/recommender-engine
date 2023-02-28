import os
import pandas as pd

from google.cloud import bigquery
from google.api_core.future import polling
from google.cloud.bigquery.retry import DEFAULT_RETRY
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

_dir = os.path.dirname(os.path.abspath(__file__))


def query_bigquery(query: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        _dir + "/bigquery_credentials.json"
    )

    client = bigquery.Client()
    query_job = client.query(query)

    query_job = client.query(query, retry=DEFAULT_RETRY)
    query_job._retry = polling.DEFAULT_RETRY
    if query_job._result_set:
        print("Succesfully queried Bigquery and got a result set")
        return query_job.result()


def return_engine():
    # SQLAlchemy connectable
    credentials_path = _dir + "/bigquery_credentials.json"
    return create_engine("bigquery://bigquery_project_id", credentials_path=credentials_path)


def return_evidence_log():
    """
    Query all articles
    """
    return pd.read_sql(
        "SELECT * FROM bigquery_project_id.analytics.articles_evidence", con=return_engine()
    )


def return_reduced_evidence_log():
    """
    Query all articles
    """
    return pd.read_sql(
        "SELECT * FROM bigquery_project_id.analytics.reduced_articles_evidence",
        con=return_engine(),
    )


def return_association_rules():
    """
    Query all rules
    """
    return pd.read_sql(
        "SELECT * FROM bigquery_project_id.analytics.association_rules_lookup", con=return_engine()
    )

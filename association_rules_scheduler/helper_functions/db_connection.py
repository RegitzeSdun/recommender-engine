import os
import pandas as pd

from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path of the parent directory
_dir = "/".join(_dir.split("/")[0:-1])


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

import logging
import os
import sys

from recommender_engine.data_layer.db_connect import query_bigquery

sys.path.insert(0, os.getcwd())

LOGGER = logging.getLogger(__name__)


def return_base_article_ids_for_specific_user(user_id):
    """Perform search in evidence log"""

    query = f"""    
    SELECT base_article_id 
    FROM `analytics.reduced_articles_evidence` 
    WHERE user_id='{user_id}'
    """

    query_result = query_bigquery(query)
    return [r["base_article_id"] for r in query_result]

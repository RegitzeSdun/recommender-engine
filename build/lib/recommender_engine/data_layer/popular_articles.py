import logging
import os
import sys

from recommender_engine.data_layer.db_connect import query_bigquery
sys.path.insert(0, os.getcwd())

LOGGER = logging.getLogger(__name__)


def return_popular_articles() -> bool:
    """Perform search in evidence log"""

    query = """    
        SELECT article_id, COUNT(*) AS number_of_articles_viewed 
        FROM `bigquery_project_id.analytics.articles_evidence` 
        WHERE article_id IS NOT NULL
        GROUP BY article_id
        ORDER BY number_of_articles_viewed desc
        LIMIT 100
    """

    query_result = query_bigquery(query)
    return [r['article_id'] for r in query_result]
    

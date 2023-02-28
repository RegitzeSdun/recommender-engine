import logging
import os
import sys

from recommender_engine.data_layer.db_connect import query_bigquery
sys.path.insert(0, os.getcwd())

LOGGER = logging.getLogger(__name__)


def return_popular_articles() -> bool:
    """Perform search in evidence log"""

    query = """    
        SELECT base_article_id, COUNT(*) AS number_of_articles_viewed 
        FROM `bigquery_project_id.analytics.reduced_articles_evidence` 
        WHERE base_article_id IS NOT NULL
        GROUP BY base_article_id
        ORDER BY number_of_articles_viewed desc
        LIMIT 100
    """

    query_result = query_bigquery(query)
    return [r['base_article_id'] for r in query_result]
    

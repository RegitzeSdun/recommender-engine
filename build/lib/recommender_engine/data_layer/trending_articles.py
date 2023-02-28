import logging
import os
import sys
from datetime import date, timedelta

from recommender_engine.data_layer.db_connect import query_bigquery
sys.path.insert(0, os.getcwd())

LOGGER = logging.getLogger(__name__)


def return_trending_articles(interval: str) -> bool:
    """Perform search in evidence log"""

    query = f"""    
        SELECT article_id, COUNT(*) AS number_of_articles_viewed 
        FROM `bigquery_project_id.analytics.articles_evidence` 
        WHERE EXTRACT(DATE from original_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL {interval} DAY) and article_id IS NOT NULL
        GROUP BY article_id
        ORDER BY number_of_articles_viewed desc
        LIMIT 100
    """

    query_result = query_bigquery(query)
    return [r['article_id'] for r in query_result]
    

import logging
from typing import Dict, Tuple, Optional, List
from collections import defaultdict
from datetime import datetime


from recommender_engine.schemas.response_schemas import (
    TrendingArticlesResponse,
)

from recommender_engine.data_layer.trending_articles import return_trending_articles

LOGGER = logging.getLogger(__name__)


def calculate_trending_articles_recommendations(trending_period: str) -> TrendingArticlesResponse:

    recommended_articles = return_trending_articles(interval=trending_period)
    
    return TrendingArticlesResponse(
        recommendations=recommended_articles,
    )


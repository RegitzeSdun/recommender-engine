import logging

from recommender_engine.schemas.response_schemas import (
    PopularArticlesResponse,
)

from recommender_engine.data_layer.popular_articles import return_popular_articles

LOGGER = logging.getLogger(__name__)


def calculate_popular_articles_recommendations() -> PopularArticlesResponse:

    recommended_articles = return_popular_articles()
    
    return PopularArticlesResponse(
        recommendations=recommended_articles,
    )


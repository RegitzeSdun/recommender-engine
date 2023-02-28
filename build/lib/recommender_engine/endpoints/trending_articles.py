import os
import sys

from fastapi import APIRouter
from fastapi_versioning import version

sys.path.insert(0, os.getcwd())


from recommender_engine.schemas.response_schemas import TrendingArticlesResponse
from recommender_engine.utils.shared_functions import get_api_version
from recommender_engine.logic_layer.trending_articles import calculate_trending_articles_recommendations

router = APIRouter()


@router.get("/trending_articles", response_model=TrendingArticlesResponse)
@version(get_api_version())
async def trending_articles_recommendations(trending_period: str = '30') -> TrendingArticlesResponse:
    """Return trending articles.
    """
    return calculate_trending_articles_recommendations(trending_period)

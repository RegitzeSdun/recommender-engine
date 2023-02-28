import os
import sys

from fastapi import APIRouter
from fastapi_versioning import version

sys.path.insert(0, os.getcwd())


from recommender_engine.schemas.response_schemas import PopularArticlesResponse
from recommender_engine.utils.shared_functions import get_api_version
from recommender_engine.logic_layer.popular_articles import calculate_popular_articles_recommendations

router = APIRouter()


@router.get("/popular_articles", response_model=PopularArticlesResponse)
@version(get_api_version())
async def popular_articles_recommendations() -> PopularArticlesResponse:
    """Return popular articles.
    """
    return calculate_popular_articles_recommendations()

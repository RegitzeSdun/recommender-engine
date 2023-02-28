import os
import sys

from fastapi import APIRouter
from fastapi_versioning import version

sys.path.insert(0, os.getcwd())


from recommender_engine.schemas.response_schemas import RecommendedForYouResponse
from recommender_engine.logic_layer.recommended_for_you import (
    calculate_recommended_for_you,
)

router = APIRouter()


@router.get("/recommended_for_you", response_model=RecommendedForYouResponse)
@version(1)
async def recommended_for_you(user_id: str) -> RecommendedForYouResponse:
    """Return popular articles."""
    return calculate_recommended_for_you(user_id)

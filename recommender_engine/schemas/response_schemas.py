import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class PopularArticlesResponse(BaseModel):
    recommendations: List[str]


class RecommendedForYouResponse(BaseModel):
    recommendations: List[Optional[str]]


class TrendingArticlesResponse(BaseModel):
    recommendations: List[str]

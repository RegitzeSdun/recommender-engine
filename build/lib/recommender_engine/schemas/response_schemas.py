import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class PopularArticlesResponse(BaseModel):
    recommendations: List[str]

class TrendingArticlesResponse(BaseModel):
    recommendations: List[str]
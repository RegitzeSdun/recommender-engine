import re
from typing import List, Optional, Union
from pydantic import BaseModel, conlist, validator, ValidationError

# Request for popular articles
class PopularArticlesInput(BaseModel):
    user_id: str



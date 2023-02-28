from email import message
import os
import sys

from fastapi.responses import JSONResponse
from fastapi import Request

sys.path.insert(0, os.getcwd())

from recommender_engine.utils.custom_exceptions import RecommenderEngineException


async def recommender_engine_exception_handler(
    request: Request, exc: RecommenderEngineException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


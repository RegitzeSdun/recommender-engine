import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

sys.path.insert(0, os.getcwd())

from recommender_engine.utils.environment_variables import load_config
from recommender_engine.utils.shared_functions import (
    get_api_version,
    create_routers_with_versions,
)

load_config(".env")

from recommender_engine.endpoints import (
    popular_articles,
    trending_articles
    )
from recommender_engine.utils.custom_error_handlers import (
    recommender_engine_exception_handler,
)
from recommender_engine.utils.custom_exceptions import RecommenderEngineException

# Create API Application
api = FastAPI()


# Add endpoints
api.include_router(popular_articles.router)
api.include_router(trending_articles.router)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app = VersionedFastAPI(api, version_format="{major}", prefix_format="/v{major}")
routers_with_versions = create_routers_with_versions(api, get_api_version())


for sub_app in app.routes:
    if hasattr(sub_app.app, "add_exception_handler"):
        sub_app.app.add_exception_handler(
            RecommenderEngineException, recommender_engine_exception_handler
        )

# Add routers with versions in the path
for route in routers_with_versions.values():
    app.routes.append(route)


if __name__ == "__main__":
    # Run FastAPI
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )

import logging
import numpy as np

from recommender_engine.schemas.response_schemas import RecommendedForYouResponse
from recommender_engine.data_layer.db_connect import return_association_rules
from recommender_engine.data_layer.recommended_for_you import (
    return_base_article_ids_for_specific_user,
)

LOGGER = logging.getLogger(__name__)


def calculate_recommended_for_you(user_id: str) -> RecommendedForYouResponse:
    association_rules_df = return_association_rules()
    base_article_ids = return_base_article_ids_for_specific_user(user_id)

    recommended_articles = list(
        set(
            association_rules_df[
                association_rules_df["antecedents"].isin(base_article_ids)
                & np.logical_not(
                    association_rules_df["consequents"].isin(base_article_ids)
                )
            ]["consequents"]
        )
    )

    return RecommendedForYouResponse(
        recommendations=recommended_articles,
    )

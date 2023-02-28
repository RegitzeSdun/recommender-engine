import os
import sys
import pandas as pd

sys.path.insert(0, os.getcwd())

"""
Functions used to clean and simplify the evidence log and prepare it for apriori analysis.
"""


def add_base_article_slug_to_df(df):
    """
    This function creates a proxy for base_article slug by taking the first slug available
    """
    article_titles_df = (
        df[["base_article_id", "slug"]]
        .drop_duplicates()
        .groupby("base_article_id")
        .slug.first()
        .reset_index()
    )
    article_titles_df = article_titles_df.rename(columns={"slug": "base_article_slug"})
    df = pd.merge(df, article_titles_df, on="base_article_id")
    return df


def reduce_df_one_transaction_per_user(df):
    """
    This function reduces the evidence log, such that there can only be one article read per user
    """
    return (
        df.groupby(["base_article_id", "base_article_slug", "user_id"])
        .original_timestamp.last()
        .reset_index()
    )


def reduce_df_to_users_with_more_than_n_articles_read(_df, min_number_of_articles_read):
    return _df[
        _df.groupby(["user_id"])["base_article_id"].transform("count")
        >= min_number_of_articles_read
    ]


def return_df_for_apriori(_df):
    """
    Function transforming df to right format for the apriori algorithm
    """

    user_transactions_df = pd.pivot_table(
        _df,
        values="original_timestamp",
        index="user_id",
        columns="base_article_id",
        aggfunc="count",
    )
    user_transactions_df = user_transactions_df.fillna(0)

    column_names = user_transactions_df.columns
    return user_transactions_df[column_names].astype(bool)

import pandas as pd

from recommender_engine.data_layer.popular_articles import return_popular_articles
from recommender_engine.data_layer.trending_articles import return_trending_articles


interval_list = range(1,30)
result = []
for day_interval in interval_list:
    trending_articles = return_trending_articles(interval=f'{day_interval} DAY')
    popular_articles = return_popular_articles()
    # compare lists
    # how many do they have in common
    articles_in_common = len(set(trending_articles).intersection(set(popular_articles)))
    # how many are on the same position
    articles_in_common_and_same_position = 0
    for i in range(len(trending_articles)):
        if trending_articles[i]==popular_articles[i]:
            articles_in_common_and_same_position += 1
    
    result.append({'day_interval':day_interval,'articles_in_common':articles_in_common,'articles_in_common_and_same_position':articles_in_common_and_same_position})

pd.DataFrame.from_records(result)
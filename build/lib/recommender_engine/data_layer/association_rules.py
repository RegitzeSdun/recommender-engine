import logging
import os
import sys
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


sys.path.insert(0, os.getcwd())
from recommender_engine.data_layer.db_connect import return_evidence_log

## Create products bought together
## https://towardsdatascience.com/apriori-association-rule-mining-explanation-and-python-implementation-290b42afdfc6

_df = return_evidence_log()

association_df = _df.groupby('user_id')['article_id'].apply(list).reset_index()
data = list(association_df['article_id'])
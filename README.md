# recommender-engine
The purpose of this repos is to provide three types of recommendations, which are accessible as get API endpoints
* most popular articles - based on all time reads
* trending articles - based on input duration, i.e. which articles have been trending the last 30 days
* recommended_for_you - based on user previous reads and apriori likelihood

All the endpoints returns base_article_ids. For more documentation go to http://0.0.0.0/docs/.

The repos is structured in the following way:

```
.
├── analysis                    # Explorative analysis of the data to set appropriate thresholds for the models
├── association_rules_scheduler # Cloud function that runs scheduled runs to build the appropriate association rules
├── recommender_engine          # Service exposing the three relevant API endpoints
├── tests                       # Test files
│   └── endpoints               # Unit tests for endpoints
├── Dockerfile                  # Builds a docker container for the recommender engine
├── README.md
├── setup.cfg                   # Specifies dependencies
└── setup.py                    # Installs dependencies
```

## Analysis

The analysis folder contains three jupyter notebooks with three separate analyses:
1. An explorative analysis of the evidence log resulting in a reduced evidence log (that dbt creates)
2. An examination of the overlap between popular and trending articles
3. Modelling of the threshold for support, confidence and the base data set for the apriori analysis


## Association rules scheduler
This is a cloud function that recalculates the apriori association rules every sunday, and updates them in bigquery.

The function is deployed by running the following command within the respective folder
```bash
gcloud functions deploy association_rules_scheduler --region=europe-west1 --entry-point main --runtime python39 --trigger-resource association_rules --trigger-event google.pubsub.topic.publish --timeout 540s --memory 1024MB
```

The cloud scheduler: trigger-update-association-rules triggers the pub/sub topic: association_rules which triggers the cloud function itself called association_rules_scheduler.

## Recommender engine
The construction of the recommender engine is based on the analyses included in the analysis folder. 

Currently, the recommended_for_you endpoint relies on the association rules, which are created by the association_rules_scheduler in the following way:
1. The reduced_evidence_log is filtered such that it only contains users that have read a specified minimum of articles
2. Frequent item sets are calculated based on this filtered data with a specified minimum support
3. The association rules are created based on the frequent items sets with a specified minimum confidence
4. The rules are uploaded to bigquery

The recommeded_for_you endpoint then works in the following way
* extracts all base_article_ids from the association rules, where the user has read antecedent but not the consequent.

For further explanation of the apriori algorithm check out analysis/3_analysis_of_association_rules.


### How to launch recommender engine locally
with Python

```bash
pip install -e .[all]
python recommender_engine/main.py
```

Run the docker file
```
docker build . -t recommender_engine -f Dockerfile
docker run -d -p 80:80 recommender_engine
```

## How to deploy the recommender engine
The deploying has been set up automatically so by commiting and pushing your code, it will automatically be deployed by cloud run. 


# Current limitations
* Tests has not yet been implemented but should
* Reconsider if pushing to git should automatically deploy a new model
* Track the performance of the endpoints
  * Implement tracking to evaluate if users likes the new categories and it makes them more liekly to click
* The recommended for you apriori analysis still needs some fine tuning. 
  * One important analysis that hasn't been done would be to calculate the amounts of recommendations we provide per user for different sets of parameters. The analysis has been initialised in 4_analysis_of_users_getting_recommendations.ipynb
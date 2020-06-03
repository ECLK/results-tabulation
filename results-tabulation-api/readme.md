# results-tabulation-api

## Prerequisites

* [Setup prerequisites](./prerequisites.html)

* [Setup auth app ](https://github.com/ECLK/auth-app)

## Get Started

**Activate the python environment**

`source ./venv/bin/activate`

**Install Dependencies**

`pip install -r requirements.txt`

**Configure database connection parameters**

Update `env/dev.cfg`

**Create Database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py create_database`

**Upgrade the Database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

**Run local server**

`export ENV_CONFIG=./env/dev.cfg && python index.py`

https://localhost:5000/ui/

**Create an election**

For testing locally, following root token can be used for the time.
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3JvbGUiOlsidGFiX2FkbWluIiwidGFiX2RhdGFfZWRpdG9yIiwidGFiX3BvbF9kaXZfcmVwX3ZpZXciLCJ0YWJfcG9sX2Rpdl9yZXBfdmVyZiIsInRhYl9lbGNfZGlzX3JlcF92aWV3IiwidGFiX2VsY19kaXNfcmVwX3ZlcmYiLCJ0YWJfbmF0X2Rpc19yZXBfdmlldyIsInRhYl9uYXRfZGlzX3JlcF92ZXJmIiwidGFiX2VjX2xlYWRlcnNoaXAiXSwiaHR0cDovL3dzbzIub3JnL2NsYWltcy91c2VybmFtZSI6ImphbmFrQGNhcmJvbi5zdXBlciIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fYWRtaW4iOiJbXSIsImp0aSI6IjI5NjYxNWJjLTIzNWQtNGU5My1hMmQ5LWY0OTM5MDE1YWU3OCIsImlhdCI6MTU5MTAyNzgxNiwiZXhwIjoxNTkxMDMxNDE2fQ.7_gyvuSxq3Af7vEGP-jBZYqmLaCFCkiurAACAXfZXks
```

Then invoke the POST `/election` with five required csv files. csv files can be found in `results-tabulation-api/ext/ExtendedElection/<ext-election-type>/sample-config-data`

eg:-

```
curl -L -X POST 'http://localhost:5000/election' \
-H 'X-Jwt-Assertion: <jwt-token-above>' \
-F 'pollingStationsDataset=@/Users/lsf/Documents/repo/results-tabulation/results-tabulation-api/ext/ExtendedElection/ExtendedElectionParliamentaryElection2020/sample-config-data/2/polling-stations-dataset.csv' \
-F 'postalCountingCentresDataset=@/Users/Documents/lsf/repo/results-tabulation/results-tabulation-api/ext/ExtendedElection/ExtendedElectionParliamentaryElection2020/sample-config-data/2/postal-counting-centres-dataset.csv' \
-F 'partyCandidatesDataset=@/Users/Documents/lsf/repo/results-tabulation/results-tabulation-api/ext/ExtendedElection/ExtendedElectionParliamentaryElection2020/sample-config-data/2/party-candidate-dataset.csv' \
-F 'invalidVoteCategoriesDataset=@/Users/Documents/lsf/repo/results-tabulation/results-tabulation-api/ext/ExtendedElection/ExtendedElectionParliamentaryElection2020/sample-config-data/2/invalid-vote-categories-dataset.csv' \
-F 'numberOfSeatsDataset=@/Users/lsf/Documents/repo/results-tabulation/results-tabulation-api/ext/ExtendedElection/ExtendedElectionParliamentaryElection2020/sample-config-data/2/number-of-seats-dataset.csv' \
-F 'electionTemplateName=PARLIAMENT_ELECTION_2020' \
-F 'electionName=PARLIAMENT ELECTION 2020'
```

**Get root token of an election**
```
curl -L -X GET 'http://localhost:5000/system-testing/election/<election-id>/root-token' \
-H 'X-Jwt-Assertion: <jwt-token-above>'
```

**Run tests**

`export ENV_CONFIG=./env/test.cfg && pytest tests`

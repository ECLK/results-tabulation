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

For testing, first a root token has to be taken. For doing this for the first time, comment out the `@authorize(required_roles=[ADMIN_ROLE])` line in `results-tabulation-api/api/ElectionApi.py`

eg:-

```
# @authorize(required_roles=[ADMIN_ROLE])
def getRootToken(electionId):
    return get_root_token(electionId=electionId)
```

Invoke the GET `/system-testing/election/{electionId}/root-token` and retrive a root token. Insert any number for electionId for the first time.

Then invoke the POST `/election` with four required csv files. csv files can be found in `results-tabulation-api/sample-data/test-4`

eg:-

```
curl -X POST \
  http://localhost:5000/election \
  -H 'X-Jwt-Assertion: <jwt-token-retrived-above>' \
  -H 'content-type: multipart/form-data' \
  -F invalidVoteCategoriesDataset=@/home/dinuka/Documents/lsf/repo/results-tabulation-tallysheets/sample-data/test-4/invalid-vote-categories.csv \
  -F partyCandidatesDataset=@/home/dinuka/Documents/lsf/repo/results-tabulation-tallysheets/sample-data/test-5/party-candidate.csv \
  -F pollingStationsDataset=@/home/dinuka/Documents/lsf/repo/results-tabulation-tallysheets/sample-data/test-5/data.csv \
  -F postalCountingCentresDataset=@/home/dinuka/Documents/lsf/repo/results-tabulation-tallysheets/sample-data/test-5/postal-data.csv \
  -F 'electionName=Test Presidential Election'
```

**Run tests**

`export ENV_CONFIG=./env/test.cfg && pytest tests`

# Election REST API

## Prerequisites

**Python 3**

**Virtual Environment**

`sudo apt install virtualenv`

`virtualenv venv --python=python3`

**My SQL**

5.7 or above

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

## Database Operations

**Initialize migration**

This is a one time thing which is required only at the project beginning. The information is only for knowledge.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db init`

**Make a revision**

If there are changes identified, a revision file is created at migrations/versions with a hash.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db migrate`

**Upgrade database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

**Merge heads**

When the commits are merged and if there are migration files merged, it's required to do this.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db merge heads`

**Drop database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database`

## API Invocation ##

**JWT generation sample**

For testing, first a root token has to be taken. 
Invoke the `/system-testing/election/{electionId}/root-token` and retrive a root token. Insert any number for the electionId for the first time.


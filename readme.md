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

**Build the Database with sample data**

`export ENV_CONFIG=./env/dev.cfg && python manage.py build_database <dataset>`

`dataset` could be `mock-election`, `test` or `test-small`

**Run local server**

`export ENV_CONFIG=./env/dev.cfg && python index.py`

https://localhost:5000/ui/

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

`export ENV_CONFIG=./env/dev.cfg && python manage.py db merge heads`

**Drop database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database`

## API Invocation ##

**JWT generation sample**

```
from jose import jwt

key = "jwt_secret"
payload = {
    'areaAssignment/dataEditor': [
        {
            "areaName": "1",
            "areaId": 7
        }
    ],
    'areaAssignment/ECLeadership': [
    ]
}
encoded = jwt.encode(payload, key)
print(encoded)
```
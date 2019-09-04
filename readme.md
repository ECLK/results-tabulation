# Election REST API

## Prerequisites

**Python 3**

**Virtual Environment**

`sudo apt install virtualenv`

`virtualenv venv --python=python3`

**My SQL**

5.7 or above

**wkhtmltopdf**

`sudo apt-get install wkhtmltopdf`


## Get Started

**Activate the python environment**

`source ./venv/bin/activate`

**Install Dependencies**

`pip install -r requirements.txt`

**Configure database connection parameters**

Update `env/dev.cfg` 

**Upgrade/create the Database**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

**Build the Database with sample data**

`export ENV_CONFIG=./env/dev.cfg && python build_database.py`

**Run local server**

`export ENV_CONFIG=./env/dev.cfg && python index.py`

https://localhost:5000/ui/

## Database Migrations

**Initialize migration**

This is a one time thing which is required only at the project beginning. The information is only for knowledge.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db init`

**Make a revision**

If there are changes identified, a revision file is created at migrations/versions with a hash.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db migrate`

**Upgrade the DB**

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

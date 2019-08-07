# Election REST API

## Prerequisites

**Python 3**

**Virtual Environment**

sudo apt install virtualenv

virtualenv venv --python=python3

source ./venv/bin/activate


**Postgresql**

https://www.postgresql.org/download/linux/ubuntu/

**wkhtmltopdf**

`sudo apt-get install wkhtmltopdf`


## Get Started

**Install Dependancies**

`pip install -r requirements.txt`

**Drop (If exists) and Create the Database**

`export ENV_CONFIG=./env/dev.cfg && python drop-and-create-database.py`

**Build the Database**

`export ENV_CONFIG=./env/dev.cfg && python build_database.py`

**Run local server**

`export ENV_CONFIG=./env/dev.cfg && python index.py`

https://localhost:5000/ui/


# Prerequisites 

## Virtual Environment

sudo apt install virtualenv

virtualenv venv --python=python3

source ./venv/bin/activate

pip install -r requirements.txt


## Postgresql

sudo apt-get install libpq-dev python-dev

https://www.postgresql.org/download/linux/ubuntu/

pgadmin4

## Api Manager

docker pull wso2/wso2am:2.6.0

docker run -it -p 8280:8280 -p 8243:8243 -p 9443:9443 --name api-manager wso2/wso2am:2.6.0

# Get Started

`python build_database.py` 

`python build_database.py`

http://localhost:5000/ui/

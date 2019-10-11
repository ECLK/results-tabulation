rm -rf ./venv 
virtualenv venv --python=python3 
source ./venv/bin/activate 
pip install -r requirements.txt 
export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database 
export ENV_CONFIG=./env/dev.cfg && python manage.py create_database
export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade 
export ENV_CONFIG=./env/dev.cfg && python manage.py build_database test
export ENV_CONFIG=./env/test.cfg && pytest tests  
export ENV_CONFIG=./env/dev.cfg && python index.py


python manage.py drop_database 
python manage.py create_database
python manage.py db upgrade 
python manage.py build_database test





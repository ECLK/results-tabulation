from flask import Flask
import sqlalchemy

app = Flask(__name__)

app.config.from_envvar('ENV_CONFIG')

engine = sqlalchemy.create_engine('%s://%s:%s@%s:%s' % (
    app.config['DATABASE_PLUGIN'],
    app.config['DATABASE_USERNAME'],
    app.config['DATABASE_PASSWORD'],
    app.config['DATABASE_HOST'],
    app.config['DATABASE_PORT']
))


def create_database():
    conn = engine.connect()
    database_name = app.config['DATABASE_NAME']

    try:
        conn.execute(f"create database {database_name}")
        print(f"Database '{database_name}' CREATED")
    except:
        print(f"Database '{database_name}' creation FAILED")
    conn.close()


def drop_database():
    conn = engine.connect()
    database_name = app.config['DATABASE_NAME']

    try:
        conn.execute(f"drop database {database_name}")
        print(f"Database '{database_name}' DROPPED")
    except:
        print(f"Database '{database_name}' not found")

    conn.close()

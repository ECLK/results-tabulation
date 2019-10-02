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
        conn.execute("create database %s" % database_name)
        print("Database '%s' CREATED" % database_name)
    except:
        print("Database '%s' creation FAILED" % database_name)
    conn.close()


def drop_database():
    conn = engine.connect()
    database_name = app.config['DATABASE_NAME']

    try:
        conn.execute("drop database %s" % database_name)
        print("Database '%s' DROPPED" % database_name)
    except:
        print("Database '%s' not found" % database_name)

    conn.close()

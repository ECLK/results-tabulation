from flask import Flask
import sqlalchemy

app = Flask(__name__)

app.config.from_envvar('ENV_CONFIG')

engine = sqlalchemy.create_engine('postgres://%s:%s@%s:%s' % (
    app.config['DATABASE_USERNAME'],
    app.config['DATABASE_PASSWORD'],
    app.config['DATABASE_HOST'],
    app.config['DATABASE_PORT']
))
conn = engine.connect()

try:
    conn.execute("commit")
    conn.execute("drop database election")
    print("Database 'election' DROPPED")
except:
    print("Database 'election' not found")

try:
    conn.execute("commit")
    conn.execute("create database election")
    print("Database 'election' CREATED")
except:
    print("Database 'election' creation FAILED")

conn.close()

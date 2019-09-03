import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from connexion.exceptions import ProblemException
import json

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)


def render_exception(exception):
    print(exception)

    db.session.rollback()

    return json.dumps({
        "detail": "",
        "status": 500,
        "title": "Internal Server Error"
    }, indent=2), 500


def render_connexion_problem_exception(connexion_exception):
    print(connexion_exception)

    db.session.rollback()
    return json.dumps({
        "detail": connexion_exception.detail,
        "status": connexion_exception.status,
        "title": connexion_exception.title
    }, indent=2), connexion_exception.status


connex_app.add_error_handler(Exception, render_exception)
connex_app.add_error_handler(ProblemException, render_connexion_problem_exception)

# Get the underlying Flask app instance
app = connex_app.app

app.config.from_envvar('ENV_CONFIG')

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s:%s/%s' % (
    app.config['DATABASE_PLUGIN'],
    app.config['DATABASE_USERNAME'],
    app.config['DATABASE_PASSWORD'],
    app.config['DATABASE_HOST'],
    app.config['DATABASE_PORT'],
    app.config['DATABASE_NAME']
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml", strict_validation=True, validate_responses=False)

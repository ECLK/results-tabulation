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
    return json.dumps({
        "detail": "",
        "status": 500,
        "title": "Internal Server Error"
    }, indent=2), 500


def render_connexion_problem_exception(connexion_exception):
    return json.dumps({
        "detail": connexion_exception.detail,
        "status": connexion_exception.status,
        "title": connexion_exception.title
    }, indent=2), connexion_exception.status


connex_app.add_error_handler(Exception, render_exception)
connex_app.add_error_handler(ProblemException, render_connexion_problem_exception)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'tallysheet.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/election'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1234@localhost:5432/election'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

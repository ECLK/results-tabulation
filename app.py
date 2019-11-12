import os
import traceback
from datetime import datetime

import connexion
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_caching import Cache

from connexion.exceptions import ProblemException
import json

db = SQLAlchemy()
ma = Marshmallow()

cache = Cache(config={
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 18144000000  # One month
})

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)


def render_exception(exception):
    error_string = traceback.format_exc()
    print(error_string)

    db.session.rollback()

    return json.dumps({
        "detail": "",
        "status": 500,
        "title": "Internal Server Error"
    }, indent=2), 500


def render_connexion_problem_exception(connexion_exception):
    error_string = traceback.format_exc()
    print(error_string)

    db.session.rollback()

    return json.dumps({
        "detail": connexion_exception.detail,
        "status": connexion_exception.status,
        "title": connexion_exception.title,
        "code": connexion_exception.args[4]
    }, indent=2), connexion_exception.status


def create_app():
    connex_app.add_error_handler(Exception, render_exception)
    connex_app.add_error_handler(
        ProblemException, render_connexion_problem_exception)

    # Get the underlying Flask app instance
    app = connex_app.app

    app.config.from_envvar('ENV_CONFIG')

    # Configure the SQLAlchemy part of the app instance
    app.config['SQLALCHEMY_ECHO'] = True

    if app.config['DATABASE_PLUGIN'] == "sqlite":
        # this is for unit tests
        app.config['SQLALCHEMY_DATABASE_URI'] = "%s://" % app.config['DATABASE_PLUGIN']
    else:
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
    db.init_app(app)

    # Initialize Marshmallow
    ma.init_app(app)

    # add CORS support
    CORS(app)

    # Read the swagger.yml file to configure the endpoints
    connex_app.add_api("swagger.yml", strict_validation=True,
                       validate_responses=False)

    @app.context_processor
    def inject_to_template():
        is_prod_env = False

        if app.config.get('PROD_ENV'):
            is_prod_env = app.config['PROD_ENV']

        from auth import get_user_name
        current_user_name = ''

        try:
            current_user_name = get_user_name()
        except:
            pass
        return dict(
            isProdEnv=is_prod_env,
            current_user=current_user_name,
            current_timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    cache.init_app(app)

    return connex_app

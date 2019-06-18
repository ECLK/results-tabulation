import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

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

import os
from config import db
from models import Person, Party

# Data to initialize database with
PEOPLE = [
    {'fname': 'Doug', 'lname': 'Farrell'},
    {'fname': 'Kent', 'lname': 'Brockman'},
    {'fname': 'Bunny','lname': 'Easter'}
]

# Delete database file if it exists currently
if os.path.exists('tallysheet.db'):
    os.remove('tallysheet.db')

# Create the database
db.create_all()

for i in range(5):
    db.session.add(Party())

db.session.commit()
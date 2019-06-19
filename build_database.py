import os
from config import db
from models import Party, Office, Electorate, Election

# Data to initialize database with
PEOPLE = [
    {'fname': 'Doug', 'lname': 'Farrell'},
    {'fname': 'Kent', 'lname': 'Brockman'},
    {'fname': 'Bunny', 'lname': 'Easter'}
]

# Delete database file if it exists currently
if os.path.exists('tallysheet.db'):
    os.remove('tallysheet.db')

# Create the database
db.create_all()

for i in range(1, 6):
    db.session.add(Party())
    db.session.add(Election())

    for j in range(1, 5):
        db.session.add(Office(electionId=i))
        db.session.add(Electorate(electionId=i))

db.session.commit()

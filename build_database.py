import os
from config import db
from models import Party, Office, Electorate, Election, Ballot, BallotBox, InvoiceItem

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

for i in range(1, 20):
    invoice_item = InvoiceItem()

    db.session.add(invoice_item)
    db.session.commit()

    db.session.add(Ballot(
        ballotId="pre-ballot-%d" % i,
        invoiceItemId=invoice_item.invoiceItemId
    ))

for i in range(1, 200):
    invoice_item = InvoiceItem()

    db.session.add(invoice_item)
    db.session.commit()

    db.session.add(BallotBox(
        ballotBoxId="pre-ballot-box-%d" % i,
        invoiceItemId=invoice_item.invoiceItemId
    ))

db.session.commit()

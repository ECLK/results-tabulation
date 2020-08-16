# Database Migrations

All the alterations of the database is done by the migration plugin called `alembic` supports for `sql-alchemy`.
Whenever any changes have been made to `sql-alchemy` modules in [orm](./orm), it has to be added to migration files
as a new revision by running a migration script.

## Make a revision

If there are changes identified, a revision file is created at migrations/versions with a hash.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db migrate`

Also, please pay attention to the database alteration changes auto generated in the revision file and make necessary 
changes in it as required.

1. If there's a new required column added to an existing entity, as update script also has to be included to fill the column for existing records.

### Sample migration file

```py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = '65900aaf5afd'
down_revision = 'a8a2fc4e4c77'
branch_labels = None
depends_on = None
db = sa


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)
    
    
    class _Election(Base):
        __tablename__ = 'election'
        electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        rootElectionId = db.Column(db.Integer,
                                   db.ForeignKey("election.electionId", name="fk_election_root_election_id"),
                                   nullable=True)
        parentElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
        isListed = db.Column(db.String(100), nullable=False)

    op.add_column('election', db.Column('isListed', db.String(length=100), nullable=False))

    existing_elections = session.query(
        _Election
    ).all()

    for election in existing_elections:
        election.isListed = election.rootElectionId == election.electionId

    session.commit()


def downgrade():
    op.drop_column('election', 'isListed')

```

## Upgrade database

`export ENV_CONFIG=./env/dev.cfg && python manage.py db upgrade`

This script will check whether the database has the latest revision and if not, update the database to the latest.

## Merge heads

When the commits are merged and if there are migration files merged, it's required to do this.

`export ENV_CONFIG=./env/dev.cfg && python manage.py db merge heads`

## Drop database

`export ENV_CONFIG=./env/dev.cfg && python manage.py drop_database`
"""empty message

Revision ID: a8a2fc4e4c77
Revises: 6a07b608d1fb
Create Date: 2019-12-05 11:59:49.849422

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = 'a8a2fc4e4c77'
down_revision = '6a07b608d1fb'
branch_labels = None
depends_on = None

Base = declarative_base()
bind = op.get_bind()
session = Session(bind=bind)


class _Election(Base):
    __tablename__ = 'election'
    electionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    rootElectionId = sa.Column(sa.Integer,
                               sa.ForeignKey("election.electionId", name="fk_election_root_election_id"),
                               nullable=True)
    parentElectionId = sa.Column(sa.Integer, sa.ForeignKey("election.electionId"), nullable=True)

    parentElection = relationship("_Election", remote_side=[electionId], foreign_keys=[parentElectionId])


def get_most_parent_election(election):
    if election.parentElection is not None:
        return get_most_parent_election(election.parentElection)
    else:
        return election


def upgrade():
    op.add_column('election', sa.Column('rootElectionId', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_election_root_election_id', 'election', 'election', ['rootElectionId'], ['electionId'])

    existing_elections = session.query(
        _Election
    ).all()

    for election in existing_elections:
        election.rootElectionId = get_most_parent_election(election).electionId

    session.commit()


def downgrade():
    op.drop_constraint('fk_election_root_election_id', 'election', type_='foreignkey')
    op.drop_column('election', 'rootElectionId')

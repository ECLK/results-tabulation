"""empty message

Revision ID: 65900aaf5afd
Revises: a8a2fc4e4c77
Create Date: 2019-12-05 12:57:21.899952

"""
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
    isListed = sa.Column(sa.String(100), nullable=False)


def upgrade():
    op.add_column('election', sa.Column('isListed', sa.String(length=100), nullable=False))

    existing_elections = session.query(
        _Election
    ).all()

    for election in existing_elections:
        election.isListed = election.rootElectionId == election.electionId

    session.commit()


def downgrade():
    op.drop_column('election', 'isListed')

"""empty message

Revision ID: 5f61093c9695
Revises: ab9d4f52637d
Create Date: 2020-03-03 21:29:02.871678

"""
from tqdm import tqdm
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

from orm.entities.Election.InvalidVoteCategory import InvalidVoteCategoryModel

revision = '5f61093c9695'
down_revision = 'ab9d4f52637d'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    op.add_column('election_invalidVoteCategory',
                  sa.Column('invalidVoteCategoryType', sa.String(length=50), nullable=True))

    print(" -- Update existing invalid vote categories which does not have a invalid vote category type.")
    existing_records = session.query(InvalidVoteCategoryModel).all()
    for existing_record in tqdm(existing_records):
        existing_record.invalidVoteCategoryType = "ELECTION"
    session.commit()


def downgrade():
    op.drop_column('election_invalidVoteCategory', 'invalidVoteCategoryType')

"""empty message

Revision ID: eb0d667f2b5e
Revises: 0718cd52821c
Create Date: 2020-02-18 07:41:20.340399

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eb0d667f2b5e'
down_revision = '0718cd52821c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('candidate', sa.Column('candidateNumber', sa.String(length=100), nullable=False))
    op.add_column('area', sa.Column('_registeredPostalVotersCount', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('candidate', 'candidateNumber')
    op.drop_column('area', '_registeredPostalVotersCount')

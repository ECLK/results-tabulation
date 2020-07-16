"""empty message

Revision ID: ed6e5567f101
Revises: a69a3f2b7e2f
Create Date: 2020-07-17 01:34:57.518764

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ed6e5567f101'
down_revision = 'a69a3f2b7e2f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('area', sa.Column('_registeredDisplacedVotersCount', sa.Integer(), nullable=True))
    op.add_column('area', sa.Column('_registeredQuarantineVotersCount', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('area', '_registeredQuarantineVotersCount')
    op.drop_column('area', '_registeredDisplacedVotersCount')

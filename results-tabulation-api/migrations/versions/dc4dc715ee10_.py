"""empty message

Revision ID: dc4dc715ee10
Revises: ed6e5567f101
Create Date: 2020-07-22 23:31:02.808042

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc4dc715ee10'
down_revision = 'ed6e5567f101'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('candidate', sa.Column('candidateType', sa.String(length=50), nullable=False))


def downgrade():
    op.drop_column('candidate', 'candidateType')

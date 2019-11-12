"""empty message

Revision ID: 8da6a3e78339
Revises: 2af9440cfc74
Create Date: 2019-11-12 19:28:02.998338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8da6a3e78339'
down_revision = '2af9440cfc74'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dashboard_status_report', sa.Column('createdAt', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('dashboard_status_report', 'createdAt')

"""empty message

Revision ID: 13c240e3ede6
Revises: ab9d4f52637d
Create Date: 2020-03-03 20:04:27.093968

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '13c240e3ede6'
down_revision = 'ab9d4f52637d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('templateRow', sa.Column('loadOnPostSave', sa.Boolean(), nullable=False))


def downgrade():
    op.drop_column('templateRow', 'loadOnPostSave')

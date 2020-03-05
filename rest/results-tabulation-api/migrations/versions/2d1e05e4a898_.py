"""empty message

Revision ID: 2d1e05e4a898
Revises: 4736e5fba8cb
Create Date: 2020-03-05 17:33:52.429519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2d1e05e4a898'
down_revision = '4736e5fba8cb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('election', sa.Column('numberOfSeatsDatasetId', sa.Integer(), nullable=True))
    op.create_foreign_key('election_fk_numberOfSeatsDatasetId', 'election', 'file', ['numberOfSeatsDatasetId'],
                          ['fileId'])


def downgrade():
    op.drop_constraint('election_fk_numberOfSeatsDatasetId', 'election', type_='foreignkey')
    op.drop_column('election', 'numberOfSeatsDatasetId')

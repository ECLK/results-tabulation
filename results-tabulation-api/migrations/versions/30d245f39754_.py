"""empty message

Revision ID: 30d245f39754
Revises: dc4dc715ee10
Create Date: 2020-08-05 21:32:53.743938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '30d245f39754'
down_revision = 'dc4dc715ee10'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('candidate', 'candidateName',
                    existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100),
                    type_=sa.String(length=250),
                    existing_nullable=False)


def downgrade():
    op.alter_column('candidate', 'candidateName',
                    existing_type=sa.String(length=250),
                    type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100),
                    existing_nullable=False)

"""empty message

Revision ID: b7b04e64002a
Revises: 30d245f39754
Create Date: 2020-08-07 13:39:28.654993

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b7b04e64002a'
down_revision = '30d245f39754'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('tallySheetVersionRow', 'numValue',
                    existing_type=mysql.FLOAT(),
                    type_=sa.DECIMAL(),
                    existing_nullable=True)


def downgrade():
    op.alter_column('tallySheetVersionRow', 'numValue',
                    existing_type=sa.DECIMAL(),
                    type_=mysql.FLOAT(),
                    existing_nullable=True)

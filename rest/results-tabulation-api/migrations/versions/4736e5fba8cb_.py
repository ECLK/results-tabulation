"""empty message

Revision ID: 4736e5fba8cb
Revises: 13c240e3ede6
Create Date: 2020-03-05 14:27:13.658927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4736e5fba8cb'
down_revision = '13c240e3ede6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'tallySheetVersionRow', 'numValue',
        existing_type=mysql.INTEGER(display_width=11),
        type_=sa.FLOAT(),
        existing_nullable=True)


def downgrade():
    op.alter_column(
        'tallySheetVersionRow', 'numValue',
        existing_type=sa.FLOAT(),
        type_=mysql.INTEGER(display_width=11),
        existing_nullable=True)

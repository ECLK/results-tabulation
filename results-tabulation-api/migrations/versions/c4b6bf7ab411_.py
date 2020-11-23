"""Drop `loadOnPostSave` column from templateRow

Revision ID: c4b6bf7ab411
Revises: e75585925c9d
Create Date: 2020-08-26 02:54:25.773982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c4b6bf7ab411'
down_revision = 'e75585925c9d'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('templateRow', 'loadOnPostSave')


def downgrade():
    op.add_column('templateRow',
                  sa.Column('loadOnPostSave', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))

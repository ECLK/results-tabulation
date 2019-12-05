"""empty message

Revision ID: 05f94f22b8fc
Revises: 4fec6cba522b
Create Date: 2019-11-11 12:09:48.701595

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '05f94f22b8fc'
down_revision = '4fec6cba522b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('dashboard_status_report', 'reportType',
                    existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
                    type_=sa.String(length=100),
                    existing_nullable=False)


def downgrade():
    op.alter_column('dashboard_status_report', 'reportType',
                    existing_type=sa.String(length=100),
                    type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
                    existing_nullable=False)

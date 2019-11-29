"""empty message

Revision ID: 4fec6cba522b
Revises: 594b586767ea
Create Date: 2019-11-10 23:04:51.556077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4fec6cba522b'
down_revision = '594b586767ea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('dashboard_status_report',
                    sa.Column('statusReportId', sa.Integer(), nullable=False),
                    sa.Column('reportType', sa.String(length=20), nullable=False),
                    sa.Column('electoralDistrictName', sa.String(length=100), nullable=False),
                    sa.Column('pollingDivisionName', sa.String(length=100), nullable=False),
                    sa.Column('status', sa.String(length=20), nullable=False),
                    sa.PrimaryKeyConstraint('statusReportId')
                    )
    op.add_column('tallySheet', sa.Column('statusReportId', sa.Integer(), nullable=True))
    op.create_foreign_key("dashboard_status_report_ibfk_1", 'tallySheet', 'dashboard_status_report', ['statusReportId'], ['statusReportId'])


def downgrade():
    op.drop_constraint("dashboard_status_report_ibfk_1", 'tallySheet', type_='foreignkey')
    op.drop_column('tallySheet', 'statusReportId')
    op.drop_table('dashboard_status_report')

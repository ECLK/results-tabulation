"""empty message

Revision ID: 2af9440cfc74
Revises: e2d779c263ea
Create Date: 2019-11-12 19:22:07.710773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2af9440cfc74'
down_revision = 'e2d779c263ea'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('dashboard_status_report_fk_election_id', 'dashboard_status_report', type_='foreignkey')
    op.alter_column('dashboard_status_report', 'electionId',
                    existing_type=mysql.INTEGER(display_width=11),
                    nullable=False)
    op.create_foreign_key("dashboard_status_report_fk_election_id", 'dashboard_status_report', 'election',
                          ['electionId'], ['electionId'])


def downgrade():
    op.drop_constraint('dashboard_status_report_fk_election_id', 'dashboard_status_report', type_='foreignkey')
    op.alter_column('dashboard_status_report', 'electionId',
                    existing_type=mysql.INTEGER(display_width=11),
                    nullable=True)
    op.create_foreign_key("dashboard_status_report_fk_election_id", 'dashboard_status_report', 'election',
                          ['electionId'], ['electionId'])

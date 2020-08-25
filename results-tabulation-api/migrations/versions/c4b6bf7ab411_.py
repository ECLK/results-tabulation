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
    op.alter_column('tallySheet', 'areaId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('tallySheet', 'electionId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('templateRow', 'loadOnPostSave')
    op.alter_column('workflowInstance', 'proofId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('workflowInstanceLog', 'proofId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)


def downgrade():
    op.alter_column('workflowInstanceLog', 'proofId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('workflowInstance', 'proofId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.add_column('templateRow', sa.Column('loadOnPostSave', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.alter_column('tallySheet', 'electionId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheet', 'areaId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)


"""empty message

Revision ID: c278f71e77a7
Revises: d2fca1ad701d
Create Date: 2019-11-05 19:35:22.813240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c278f71e77a7'
down_revision = 'd2fca1ad701d'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dashboard_status_PRE_34', sa.Column('candidateId', sa.Integer(), nullable=True))
    op.add_column('dashboard_status_PRE_34', sa.Column('secondPreferenceCount', sa.Integer(), nullable=False))
    op.add_column('dashboard_status_PRE_34', sa.Column('thirdPreferenceCount', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'dashboard_status_PRE_34', 'candidate', ['candidateId'], ['candidateId'])
    op.drop_column('dashboard_status_PRE_34', 'candidate1Preference3Count')
    op.drop_column('dashboard_status_PRE_34', 'candidate2Preference3Count')
    op.drop_column('dashboard_status_PRE_34', 'candidate2Preference2Count')
    op.drop_column('dashboard_status_PRE_34', 'candidate1Preference2Count')
    op.alter_column('election_candidate', 'qualifiedForPreferences',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('invoice', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('invoice', 'delete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('invoice_stationaryItem', 'received',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('proof', 'finished',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('proof', 'finished',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('invoice_stationaryItem', 'received',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('invoice', 'delete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('invoice', 'confirmed',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('election_candidate', 'qualifiedForPreferences',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.add_column('dashboard_status_PRE_34', sa.Column('candidate1Preference2Count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('dashboard_status_PRE_34', sa.Column('candidate2Preference2Count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('dashboard_status_PRE_34', sa.Column('candidate2Preference3Count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('dashboard_status_PRE_34', sa.Column('candidate1Preference3Count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'dashboard_status_PRE_34', type_='foreignkey')
    op.drop_column('dashboard_status_PRE_34', 'thirdPreferenceCount')
    op.drop_column('dashboard_status_PRE_34', 'secondPreferenceCount')
    op.drop_column('dashboard_status_PRE_34', 'candidateId')
    ### end Alembic commands ###

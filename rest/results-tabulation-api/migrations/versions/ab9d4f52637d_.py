"""empty message

Revision ID: ab9d4f52637d
Revises: 7bdab37d8bbf
Create Date: 2020-03-01 14:18:08.708158

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab9d4f52637d'
down_revision = '7bdab37d8bbf'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('election', 'isListed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
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
    op.alter_column('tallySheet', 'metaId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.add_column('tallySheetVersionRow', sa.Column('invalidVoteCategoryId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tallySheetVersionRow', 'election_invalidVoteCategory', ['invalidVoteCategoryId'], ['invalidVoteCategoryId'])
    op.alter_column('templateRow', 'hasMany',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('templateRow', 'isDerived',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('templateRowColumn', 'grouped',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('templateRowColumn', 'grouped',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('templateRow', 'isDerived',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('templateRow', 'hasMany',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.drop_constraint(None, 'tallySheetVersionRow', type_='foreignkey')
    op.drop_column('tallySheetVersionRow', 'invalidVoteCategoryId')
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('tallySheet', 'metaId',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
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
    op.alter_column('election', 'isListed',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    ### end Alembic commands ###
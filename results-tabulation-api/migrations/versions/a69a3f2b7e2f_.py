"""empty message

Revision ID: a69a3f2b7e2f
Revises: c23aa9b6b6e1
Create Date: 2020-07-12 17:52:44.868130

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a69a3f2b7e2f'
down_revision = 'c23aa9b6b6e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tallySheetVersion', sa.Column('exportedLetterPdfFileId', sa.Integer(), nullable=True))
    op.create_foreign_key('tallySheetVersion_fk_exportedLetterPdfFileId', 'tallySheetVersion', 'file',
                          ['exportedLetterPdfFileId'], ['fileId'])


def downgrade():
    op.drop_constraint('tallySheetVersion_fk_exportedLetterPdfFileId', 'tallySheetVersion', type_='foreignkey')
    op.drop_column('tallySheetVersion', 'exportedLetterPdfFileId')

"""empty message

Revision ID: c23aa9b6b6e1
Revises: b159e6f82036
Create Date: 2020-06-29 01:05:56.493877

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c23aa9b6b6e1'
down_revision = 'b159e6f82036'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tallySheetVersion', sa.Column('exportedPdfFileId', sa.Integer(), nullable=True))
    op.create_foreign_key('tallySheetVersion_fk_exportedPdfFileId', 'tallySheetVersion', 'file', ['exportedPdfFileId'],
                          ['fileId'])


def downgrade():
    op.drop_constraint('tallySheetVersion_fk_exportedPdfFileId', 'tallySheetVersion', type_='foreignkey')
    op.drop_column('tallySheetVersion', 'exportedPdfFileId')

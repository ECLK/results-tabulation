"""empty message

Revision ID: 7b90e0131061
Revises: 54905bcc8d5b
Create Date: 2019-09-18 14:12:21.154560

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b90e0131061'
down_revision = '54905bcc8d5b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('tallySheet', 'tallySheetCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34_RO', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)

    op.alter_column('tallySheetVersion', 'tallySheetVersionCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34_RO', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)


def downgrade():
    op.alter_column('tallySheet', 'tallySheetCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_ED',
                                             'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO', 'PRE_34_RO',
                                             'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS', 'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)

    op.alter_column('tallySheetVersion', 'tallySheetVersionCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_ED',
                                             'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO', 'PRE_34_RO',
                                             'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS', 'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)

"""empty message

Revision ID: 4908a7e83f30
Revises: 6ccbf5b045e3
Create Date: 2019-11-05 21:30:36.524969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4908a7e83f30'
down_revision = '6ccbf5b045e3'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('tallySheet', 'tallySheetCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)

    op.alter_column('tallySheetVersion', 'tallySheetVersionCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS'),
                    nullable=False)


def downgrade():
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

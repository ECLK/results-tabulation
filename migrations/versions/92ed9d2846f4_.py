"""empty message

Revision ID: 92ed9d2846f4
Revises: 33416ebc286c
Create Date: 2019-11-08 18:51:07.284715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '92ed9d2846f4'
down_revision = '33416ebc286c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('tallySheet', 'tallySheetCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS', 'PRE_34_PD', 'PRE_34_ED', 'PRE_34_AI'),
                    nullable=False)

    op.alter_column('tallySheetVersion', 'tallySheetVersionCode',
                    existing_type=mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD', 'PRE_30_PD_PV',
                                             'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO', 'PRE_34_II_RO',
                                             'PRE_34', 'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                                             'PRE_ALL_ISLAND_RESULTS', 'PRE_34_PD', 'PRE_34_ED', 'PRE_34_AI'),
                    nullable=False)


def downgrade():
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

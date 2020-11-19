"""Adding `administrativeDistrictId` and `provinceId` to the areaMap table

Revision ID: 737405461d37
Revises: c4b6bf7ab411
Create Date: 2020-10-28 01:37:32.338900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '737405461d37'
down_revision = 'c4b6bf7ab411'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('area_map', sa.Column('administrativeDistrictId', sa.Integer(), nullable=True))
    op.add_column('area_map', sa.Column('provinceId', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_area_map_provinceId_area'), 'area_map', 'area', ['provinceId'], ['areaId'])
    op.create_foreign_key(op.f('fk_area_map_administrativeDistrictId_area'), 'area_map', 'area',
                          ['administrativeDistrictId'], ['areaId'])


def downgrade():
    op.drop_constraint(op.f('fk_area_map_administrativeDistrictId_area'), 'area_map', type_='foreignkey')
    op.drop_constraint(op.f('fk_area_map_provinceId_area'), 'area_map', type_='foreignkey')
    op.drop_column('area_map', 'provinceId')
    op.drop_column('area_map', 'administrativeDistrictId')

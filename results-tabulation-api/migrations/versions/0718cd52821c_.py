"""empty message

Revision ID: 0718cd52821c
Revises: 5d7ed731c34a
Create Date: 2020-02-16 10:41:41.309870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

# revision identifiers, used by Alembic.
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_QUERY, TALLY_SHEET_COLUMN_SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT

revision = '0718cd52821c'
down_revision = '5d7ed731c34a'
branch_labels = None
depends_on = None


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    op.add_column('templateRowColumn', sa.Column('source', sa.String(length=50), nullable=True))

    class _TemplateRow(Base):
        __tablename__ = 'templateRow'
        templateRowId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        templateId = sa.Column(sa.Integer, sa.ForeignKey("template.templateId"))
        templateRowType = sa.Column(sa.String(200), nullable=False)
        hasMany = sa.Column(sa.Boolean, nullable=False, default=False)
        isDerived = sa.Column(sa.Boolean, nullable=False, default=False)

    class _TemplateRowColumn(Base):
        __tablename__ = 'templateRowColumn'
        templateRowColumnId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        templateRowId = sa.Column(sa.Integer, sa.ForeignKey("templateRow.templateRowId"))
        templateRowColumnName = sa.Column(sa.String(200), nullable=False)
        source = sa.Column(sa.String(50), nullable=False)
        grouped = sa.Column(sa.Boolean, default=False, nullable=False)
        func = sa.Column(sa.String(200), nullable=True)

    print(" -- Update existing derived template row column's source to 'Query'.")
    existing_derived_template_rows = session.query(_TemplateRow).filter(_TemplateRow.isDerived == True).all()
    for existing_derived_template_row in tqdm(existing_derived_template_rows):
        existing_derived_template_row_columns = session.query(_TemplateRowColumn).filter(
            _TemplateRowColumn.templateRowId == existing_derived_template_row.templateRowId
        ).all()
        for existing_derived_template_row_column in existing_derived_template_row_columns:
            existing_derived_template_row_column.source = TALLY_SHEET_COLUMN_SOURCE_QUERY
            session.add(existing_derived_template_row_column)

        session.commit()

    print(" -- Update existing not derived template row column's source to 'Content' and 'Meta' accordingly.")
    existing_not_derived_template_rows = session.query(_TemplateRow).filter(_TemplateRow.isDerived == False).all()
    existing_meta_column_names = ["areaId", "electionId"]
    for existing_not_derived_template_row in tqdm(existing_not_derived_template_rows):
        existing_not_derived_template_row_columns = session.query(_TemplateRowColumn).filter(
            _TemplateRowColumn.templateRowId == existing_not_derived_template_row.templateRowId
        ).all()
        for existing_not_derived_template_row_column in existing_not_derived_template_row_columns:
            if existing_not_derived_template_row_column.templateRowColumnName in existing_meta_column_names:
                existing_not_derived_template_row_column.source = TALLY_SHEET_COLUMN_SOURCE_META
            else:
                existing_not_derived_template_row_column.source = TALLY_SHEET_COLUMN_SOURCE_CONTENT
            session.add(existing_not_derived_template_row_column)

        session.commit()

    op.alter_column(
        'templateRowColumn', 'source',
        existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50),
        nullable=False)


def downgrade():
    op.drop_column('templateRowColumn', 'source')

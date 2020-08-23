"""empty message

Revision ID: e75585925c9d
Revises: fddd82f918b7
Create Date: 2020-08-23 18:33:24.453875

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

# revision identifiers, used by Alembic.
revision = 'e75585925c9d'
down_revision = 'fddd82f918b7'
branch_labels = None
depends_on = None

Base = declarative_base()
bind = op.get_bind()
session = Session(bind=bind)
db = sa


def upgrade():
    op.add_column('templateRow_derivativeTemplateRow',
                  sa.Column('derivativeTemplateName', sa.String(length=100), nullable=False))
    op.add_column('templateRow_derivativeTemplateRow',
                  sa.Column('derivativeTemplateRowType', sa.String(length=200), nullable=False))

    class _Template(Base):
        __tablename__ = 'template'
        templateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        templateName = db.Column(db.String(100), nullable=False)

    class _TemplateRow(Base):
        __tablename__ = 'templateRow'
        templateRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        templateId = db.Column(db.Integer, db.ForeignKey("template.templateId"))
        templateRowType = db.Column(db.String(200), nullable=False)
        hasMany = db.Column(db.Boolean, nullable=False, default=False)
        isDerived = db.Column(db.Boolean, nullable=False, default=False)

    class _TemplateRow_DerivativeTemplateRow(Base):
        __tablename__ = 'templateRow_derivativeTemplateRow'
        templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True)
        derivativeTemplateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True)
        derivativeTemplateName = db.Column(db.String(100), nullable=False)
        derivativeTemplateRowType = db.Column(db.String(200), nullable=False)

    print(" -- Update existing derivative template rows.")
    derivative_template_rows = session.query(_TemplateRow_DerivativeTemplateRow).all()
    for derivative_template_row in tqdm(derivative_template_rows):
        additional_mappings = session.query(
            _Template.templateName.label("derivativeTemplateName"),
            _TemplateRow.templateRowType.label("derivativeTemplateRowType")
        ).filter(
            _TemplateRow.templateRowId == derivative_template_row.derivativeTemplateRowId,
            _Template.templateId == _TemplateRow.templateId
        ).one_or_none()

        derivative_template_row.derivativeTemplateName = additional_mappings.derivativeTemplateName
        derivative_template_row.derivativeTemplateRowType = additional_mappings.derivativeTemplateRowType

        session.add(derivative_template_row)

    session.commit()

    op.drop_constraint('templateRow_derivativeTemplateRow_ibfk_1', 'templateRow_derivativeTemplateRow',
                       type_='foreignkey')
    op.drop_constraint('templateRow_derivativeTemplateRow_ibfk_2', 'templateRow_derivativeTemplateRow',
                       type_='foreignkey')

    op.execute('ALTER TABLE templateRow_derivativeTemplateRow DROP PRIMARY KEY')

    op.create_foreign_key('templateRow_derivativeTemplateRow_ibfk_2', 'templateRow_derivativeTemplateRow',
                          'templateRow', ['templateRowId'], ['templateRowId'])

    op.create_primary_key('pk_templateRow_derivativeTemplateRow', 'templateRow_derivativeTemplateRow',
                          ['templateRowId', 'derivativeTemplateName', 'derivativeTemplateRowType'])

    op.drop_column('templateRow_derivativeTemplateRow', 'derivativeTemplateRowId')


def downgrade():
    op.add_column('templateRow_derivativeTemplateRow',
                  sa.Column('derivativeTemplateRowId', mysql.INTEGER(display_width=11), autoincrement=False,
                            nullable=False))
    op.create_foreign_key('templateRow_derivativeTemplateRow_ibfk_1', 'templateRow_derivativeTemplateRow',
                          'templateRow', ['derivativeTemplateRowId'], ['templateRowId'])
    op.drop_column('templateRow_derivativeTemplateRow', 'derivativeTemplateRowType')
    op.drop_column('templateRow_derivativeTemplateRow', 'derivativeTemplateName')

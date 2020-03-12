from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from constants import TALLY_SHEET_COLUMN_SOURCE
from ext import ExtendedTallySheet
from app import db


class TemplateModel(db.Model):
    __tablename__ = 'template'

    templateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    templateName = db.Column(db.String(100), nullable=False)

    rows = relationship("TemplateRowModel")

    @hybrid_property
    def isDerived(self):
        if self.has_data_entry():
            return False
        else:
            return True

    def has_data_entry(self):
        has_data_entry = False
        for row in self.rows:
            if row.isDerived is False:
                has_data_entry = True

        return has_data_entry

    def is_submit_allowed(self):
        return self.has_data_entry()

    def __init__(self, templateName):
        super(TemplateModel, self).__init__(
            templateName=templateName
        )

        db.session.add(self)
        db.session.flush()

    def add_row(self, templateRowType, hasMany=False, isDerived=False, loadOnPostSave=False, columns=[]):
        templateRow = TemplateRowModel(
            templateId=self.templateId,
            templateRowType=templateRowType,
            hasMany=hasMany,
            isDerived=isDerived,
            loadOnPostSave=loadOnPostSave
        )

        for column in columns:
            templateRow.add_column(column["columnName"], source=column["source"], grouped=column["grouped"],
                                   func=column["func"])

        return templateRow


Model = TemplateModel


class TemplateRowModel(db.Model):
    __tablename__ = 'templateRow'
    templateRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    templateId = db.Column(db.Integer, db.ForeignKey("template.templateId"))
    templateRowType = db.Column(db.String(200), nullable=False)
    hasMany = db.Column(db.Boolean, nullable=False, default=False)
    isDerived = db.Column(db.Boolean, nullable=False, default=False)
    loadOnPostSave = db.Column(db.Boolean, nullable=False, default=False)

    derivativeTemplateRows = relationship(
        "TemplateRowModel", secondary="templateRow_derivativeTemplateRow", lazy="subquery",
        primaryjoin="TemplateRowModel.templateRowId==TemplateRow_DerivativeTemplateRow_Model.derivativeTemplateRowId",
        secondaryjoin="TemplateRow_DerivativeTemplateRow_Model.templateRowId==TemplateRowModel.templateRowId"
    )

    columns = relationship("TemplateRowColumnModel")

    def __init__(self, templateId, templateRowType, hasMany=False, isDerived=False, loadOnPostSave=False):
        super(TemplateRowModel, self).__init__(
            templateId=templateId,
            templateRowType=templateRowType,
            hasMany=hasMany,
            isDerived=isDerived,
            loadOnPostSave=loadOnPostSave
        )

        db.session.add(self)
        db.session.flush()

    def add_derivative_template_row(self, derivativeTemplateRow):
        TemplateRow_DerivativeTemplateRow_Model(
            self.templateRowId,
            derivativeTemplateRow.templateRowId
        )

        return self

    def add_column(self, templateRowColumnName, source=TALLY_SHEET_COLUMN_SOURCE.TALLY_SHEET_COLUMN_SOURCE_CONTENT,
                   grouped=False, func=None):
        return TemplateRowColumnModel(
            templateRow=self,
            templateRowColumnName=templateRowColumnName,
            grouped=grouped,
            func=func,
            source=source
        )


class TemplateRowColumnModel(db.Model):
    __tablename__ = 'templateRowColumn'
    templateRowColumnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"))
    templateRowColumnName = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(50), nullable=False)  # Meta, Content, Query
    grouped = db.Column(db.Boolean, default=False, nullable=False)
    func = db.Column(db.String(200), nullable=True)

    def __init__(self, templateRow, templateRowColumnName,
                 source=TALLY_SHEET_COLUMN_SOURCE.TALLY_SHEET_COLUMN_SOURCE_CONTENT, grouped=False, func=None):
        super(TemplateRowColumnModel, self).__init__(
            templateRowId=templateRow.templateRowId,
            templateRowColumnName=templateRowColumnName,
            source=source,
            grouped=grouped,
            func=func
        )

        db.session.add(self)
        db.session.flush()


class TemplateRow_DerivativeTemplateRow_Model(db.Model):
    __tablename__ = 'templateRow_derivativeTemplateRow'
    templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True)
    derivativeTemplateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True)

    def __init__(self, templateRowId, derivativeTemplateRowId):
        super(TemplateRow_DerivativeTemplateRow_Model, self).__init__(
            templateRowId=templateRowId,
            derivativeTemplateRowId=derivativeTemplateRowId
        )

        db.session.add(self)
        db.session.flush()


def create(templateName):
    result = Model(
        templateName=templateName
    )

    return result


def get(templateName):
    result = Model.query.filter(
        Model.templateName == templateName
    ).one_or_none()

    return result

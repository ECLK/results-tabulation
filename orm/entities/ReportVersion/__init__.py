from app import db
from sqlalchemy.orm import relationship
from flask import render_template
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, File, Report, HistoryVersion
from orm.enums import ReportCodeEnum


class ReportVersionModel(db.Model):
    __tablename__ = 'reportVersion'
    reportVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId),
                                primary_key=True)
    reportId = db.Column(db.Integer, db.ForeignKey(Report.Model.__table__.c.reportId))
    reportFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId), nullable=True)

    report = relationship(Report.Model, foreign_keys=[reportId])
    historyVersion = relationship(HistoryVersion.Model, foreign_keys=[reportVersionId])
    reportFile = relationship(File.Model, foreign_keys=[reportFileId])

    reportCode = association_proxy("report", "reportCode")
    createdBy = association_proxy("historyVersion", "createdBy")
    createdAt = association_proxy("historyVersion", "createdAt")


Model = ReportVersionModel


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    report = Report.get_by_id(reportId)
    report = Report.Model()

    html = render_template(
        'test-report-template.html',
        title="Test Template",
        data=[
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]
    )

    fileName = ""
    if report.electorateId is None:
        fileName = "[PRE-41][%s][%s]" % (report.office.officeType, report.office.officeName)
    else:
        fileName = "[PRE-41][%s][%s]" % (report.electorate.electorateType, report.electorate.electorateName)

    reportFile = File.createReport(
        fileName=fileName,
        html=html
    )

    result = Model(
        reportId=reportId,
        reportFileId=reportFile.fileId
    )

    db.session.add(result)
    db.session.commit()

    return result

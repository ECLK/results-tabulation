from app import db
from sqlalchemy.orm import relationship
from flask import render_template
from sqlalchemy.ext.associationproxy import association_proxy

from exception import NotFoundException
from orm.entities import Election, File, Report, HistoryVersion, SubmissionVersion
from orm.enums import ReportCodeEnum


class ReportVersionModel(db.Model):
    __tablename__ = 'reportVersion'

    reportVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                primary_key=True)
    reportVersionCode = db.Column(db.Enum(ReportCodeEnum), nullable=False)
    reportFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId), nullable=False)

    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[reportVersionId])
    reportFile = relationship(File.Model, foreign_keys=[reportFileId])

    submission = association_proxy("submissionVersion", "submission")
    reportId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")

    __mapper_args__ = {
        'polymorphic_on': reportVersionCode
    }


Model = ReportVersionModel


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def get_report_filename(report):
    return "PRE-41-%s-%s.pdf" % (report.area.areaType.name, report.area.areaName)


def create(reportId, html):
    report = Report.get_by_id(reportId=reportId)
    if report is None:
        raise NotFoundException("Report not found. (reportId=%d)" % reportId)

    submissionVersion = SubmissionVersion.create(submissionId=reportId)

    reportFile = File.createReport(
        fileName=get_report_filename(report),
        html=html
    )

    result = Model(
        reportVersionId=submissionVersion.submissionVersionId,
        reportFileId=reportFile.fileId,
        reportVersionCode=report.reportCode
    )

    db.session.add(result)
    db.session.commit()

    return result

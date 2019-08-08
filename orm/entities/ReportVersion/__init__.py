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
    reportFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId), nullable=False)

    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[reportVersionId])
    reportFile = relationship(File.Model, foreign_keys=[reportFileId])

    reportId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")


Model = ReportVersionModel


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    report = Report.get_by_id(reportId=reportId)
    if report is None:
        raise NotFoundException("Report not found. (reportId=%d)" % reportId)

    submissionVersion = SubmissionVersion.create(submissionId=reportId)

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

    if report.submission.electorate is None:
        fileName = "PRE-41-%s-%s.pdf" % (report.office.officeType.name, report.office.officeName)
    else:
        fileName = "PRE-41-%s-%s.pdf" % (report.electorate.electorateType.name, report.electorate.electorateName)

    reportFile = File.createReport(
        fileName=fileName,
        html=html
    )

    result = Model(
        reportVersionId=submissionVersion.submissionVersionId,
        reportFileId=reportFile.fileId
    )

    db.session.add(result)
    db.session.commit()

    return result

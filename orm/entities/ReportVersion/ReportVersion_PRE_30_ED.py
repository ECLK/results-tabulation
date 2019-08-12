from app import db
from sqlalchemy.orm import relationship
from flask import render_template
from sqlalchemy.ext.associationproxy import association_proxy

from exception import NotFoundException
from orm.entities import Election, File, Report, HistoryVersion, SubmissionVersion, ReportVersion
from orm.enums import ReportCodeEnum


class ReportVersion_PRE_30_ED_Model(ReportVersion.Model):
    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_ED
    }


Model = ReportVersion_PRE_30_ED_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    html = render_template(
        'test-report-template.html',
        title="Test Template PRE-30-ED",
        data=[
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]
    )

    return ReportVersion.create(reportId=reportId, html=html)

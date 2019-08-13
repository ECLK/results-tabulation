from flask import render_template

from orm.entities import ReportVersion
from orm.enums import ReportCodeEnum


class ReportVersion_PRE_30_PD_Model(ReportVersion.Model):
    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_PD
    }


Model = ReportVersion_PRE_30_PD_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    html = render_template(
        'test-report-template.html',
        title="Test Template PRE-30-PD",
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

from app import db
from sqlalchemy.orm import relationship
from flask import render_template
from sqlalchemy.ext.associationproxy import association_proxy

from exception import NotFoundException
from orm.entities import Election, File, Report, HistoryVersion, SubmissionVersion, ReportVersion, Electorate
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_41_Model(ReportVersion.Model):
    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_41
    }


Model = ReportVersion_PRE_41_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    report = Report.get_by_id(reportId=reportId)
    data = []

    electorates = Electorate.get_all(
        electionId=report.electionId,
        electorateType=AreaTypeEnum.ElectoralDistrict
    )

    for electoralDistrict in electorates:
        for pollingDivision in electoralDistrict.children:
            for pollingDistrict in pollingDivision.children:
                # for pollingStation in pollingDistrict.pollingStations:
                data.append([
                    electoralDistrict.electorateName,
                    pollingDivision.electorateName,
                    pollingDistrict.electorateName,
                    # pollingStation.officeName,
                    # pollingStation.parentOffice.officeName,
                    # pollingStation.parentOffice.parentOffice.officeName,
                ])

    html = render_template(
        'test-report-template.html',
        title="Test Template PRE-30-ED",
        data=data
    )

    return ReportVersion.create(reportId=reportId, html=html)

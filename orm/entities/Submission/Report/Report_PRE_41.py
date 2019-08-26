from orm.entities import Report
from orm.enums import ReportCodeEnum

from util import get_paginated_query


class Report_PRE_41_Model(Report.Model):
    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_41
    }


Model = Report_PRE_41_Model


def get_by_id(reportId):
    result = Model.query.filter(
        Model.reportId == reportId
    ).one_or_none()

    return result


def get_all(electionId=None, officeId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if officeId is not None:
        query = query.filter(Model.officeId == officeId)

    result = get_paginated_query(query).all()

    return result


def create(electionId, areaId):
    result = Model(
        electionId=electionId,
        areaId=areaId
    )

    return result

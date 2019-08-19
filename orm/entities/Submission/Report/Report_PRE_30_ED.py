from exception import ForbiddenException, NotFoundException, MethodNotAllowedException
from orm.entities import Report
from orm.entities.Area.Electorate import PollingDistrict, PollingDivision, ElectoralDistrict
from orm.entities.Submission import TallySheet
from orm.enums import ReportCodeEnum, TallySheetCodeEnum
from sqlalchemy.ext.hybrid import hybrid_property

from util import get_paginated_query


class Report_PRE_30_ED_Model(Report.Model):

    def __init__(self, electionId, areaId):
        area = ElectoralDistrict.get_by_id(electoralDistrictId=areaId)

        if area is None:
            raise NotFoundException("Electoral district not found (areaId=%d)" % areaId)

        super(Report_PRE_30_ED_Model, self).__init__(electionId=electionId, areaId=areaId)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_ED
    }


Model = Report_PRE_30_ED_Model


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

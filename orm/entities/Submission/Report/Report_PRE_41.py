from exception import ForbiddenException, NotFoundException, MethodNotAllowedException
from orm.entities import Report
from orm.entities.Submission import TallySheet
from orm.enums import ReportCodeEnum, TallySheetCodeEnum
from sqlalchemy.ext.hybrid import hybrid_property

from util import get_paginated_query


class Report_PRE_41_Model(Report.Model):

    @hybrid_property
    def tallySheet(self):
        tallySheetId = self.children[0].submissionId
        return TallySheet.get_by_id(tallySheetId=tallySheetId)

    def __init__(self, reportCode, electionId, areaId, tallySheetId):
        if tallySheetId is None:
            raise ForbiddenException("PRE-41 report must be associated with exactly one PRE-41 tally sheet.")

        child_tally_sheet = TallySheet.get_by_id(tallySheetId)

        if child_tally_sheet is None:
            raise NotFoundException("No tally sheet found associated with the given id (tallySheetId=%d).",
                                    tallySheetId)
        elif child_tally_sheet.tallySheetCode is not TallySheetCodeEnum.PRE_41:
            raise NotFoundException("Given tally sheet is not PRE-41 (tallySheetId=%d).", tallySheetId)

        super(Report_PRE_41_Model, self).__init__(reportCode=reportCode, electionId=electionId, areaId=areaId)

        self.submission.add_child(tallySheetId)

    def add_child(self, childId):
        raise MethodNotAllowedException("Only one tally sheet is allowed to be the child of PRE-41 report.")

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


def create(reportCode, electionId, areaId, tallySheetId):
    result = Model(
        reportCode=reportCode,
        electionId=electionId,
        areaId=areaId,
        tallySheetId=tallySheetId
    )

    return result

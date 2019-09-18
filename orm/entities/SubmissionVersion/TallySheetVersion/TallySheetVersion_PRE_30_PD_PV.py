from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func, and_

from app import db
from exception import NotFoundException
from orm.entities import Area, Candidate, Party, Submission
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_30_PD
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD
from util import get_paginated_query

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum


class TallySheetVersion_PRE_30_PD_PV_Model(TallySheetVersion_PRE_30_PD.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_30_PD_PV_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_30_PD_PV
    }

    def add_row(self, countingCentreId, candidateId, count):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD

        TallySheetVersionRow_PRE_30_PD.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            countingCentreId=countingCentreId,
            count=count
        )

    @hybrid_property
    def countingCentres(self):
        return self.submission.area.get_associated_areas(AreaTypeEnum.PostalVoteCountingCentre)


Model = TallySheetVersion_PRE_30_PD_PV_Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_30_PD_PV:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result

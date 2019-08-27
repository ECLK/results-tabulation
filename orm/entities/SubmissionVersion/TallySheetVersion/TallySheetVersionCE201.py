from sqlalchemy.orm import relationship

from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion
from util import get_paginated_query

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum


class TallySheetVersionCE201Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersionCE201Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.CE_201
    }

    def add_row(self, areaId, ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused,
                 boxCountOrdinary, boxCountTendered, ballotPaperAccountOrdinary, ballotPaperAccountTendered):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201

        return TallySheetVersionRow_CE_201.create(
            tallySheetVersion=self,
            areaId=areaId,
            ballotsIssued=ballotsIssued,
            ballotsReceived=ballotsReceived,
            ballotsSpoilt=ballotsSpoilt,
            ballotsUnused=ballotsUnused,
            boxCountOrdinary=boxCountOrdinary,
            boxCountTendered=boxCountTendered,
            ballotPaperAccountOrdinary=ballotPaperAccountOrdinary,
            ballotPaperAccountTendered=ballotPaperAccountTendered
        )

    content = relationship("TallySheetVersionRow_CE_201_Model")


Model = TallySheetVersionCE201Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.CE_201:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result

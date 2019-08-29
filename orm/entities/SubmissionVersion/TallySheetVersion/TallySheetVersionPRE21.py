from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from exception import NotFoundException
from orm.entities import Candidate, Party
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_21
from util import get_paginated_query

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum
from sqlalchemy import and_


class TallySheetVersionPRE21Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersionPRE21Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_21
    }

    def add_row(self, count, invalidVoteCategoryId=None):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_21

        TallySheetVersionRow_PRE_21.create(
            tallySheetVersionId=self.tallySheetVersionId,
            count=count,
            invalidVoteCategoryId=invalidVoteCategoryId
        )

    @hybrid_property
    def content(self):
        return db.session.query(
            InvalidVoteCategory.Model.invalidVoteCategoryId,
            InvalidVoteCategory.Model.categoryDescription,
            TallySheetVersionRow_PRE_21.Model.count
        ).join(
            TallySheetVersionRow_PRE_21.Model,
            and_(
                TallySheetVersionRow_PRE_21.Model.invalidVoteCategoryId == InvalidVoteCategory.Model.invalidVoteCategoryId,
                TallySheetVersionRow_PRE_21.Model.tallySheetVersionId == self.tallySheetVersionId
            ),
            isouter=True
        ).filter(
            InvalidVoteCategory.Model.electionId == self.submission.electionId
        )


Model = TallySheetVersionPRE21Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_21:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result

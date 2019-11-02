from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_CO, TallySheetVersionRow_RejectedVoteCount
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_34_CO_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_CO_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_CO
    }

    def add_row(self, candidateId, notCountedBallotPapers, remainingBallotPapers):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_CO
        return TallySheetVersionRow_PRE_34_CO.create(
            candidateId=candidateId,
            tallySheetVersionId=self.tallySheetVersionId,
            notCountedBallotPapers=notCountedBallotPapers,
            remainingBallotPapers=remainingBallotPapers
        )


Model = TallySheetVersion_PRE_34_CO_Model

from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from exception import NotFoundException
from orm.entities.Election import ElectionCandidate
from orm.entities.Result.CandidateWiseResult import CandidateCount
from util import get_paginated_query

from orm.entities import SubmissionVersion
from orm.entities.Submission import TallySheet
from orm.entities.Result import CandidateWiseResult
from orm.enums import TallySheetCodeEnum


class TallySheetVersionPRE41Model(db.Model):
    __tablename__ = 'tallySheetVersion_PRE41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    candidateWiseResultId = db.Column(db.Integer,
                                      db.ForeignKey(CandidateWiseResult.Model.__table__.c.candidateWiseResultId))

    candidateWiseResult = relationship(CandidateWiseResult.Model, foreign_keys=[candidateWiseResultId])
    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])

    submission = association_proxy("submissionVersion", "submission")
    tallySheetId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")

    @hybrid_property
    def tallySheetContent(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            CandidateCount.Model.count,
            CandidateCount.Model.countInWords,
            CandidateCount.Model.candidateWiseResultId
        ).join(
            CandidateCount.Model,
            CandidateCount.Model.candidateId == ElectionCandidate.Model.candidateId,
        ).filter(
            CandidateCount.Model.candidateWiseResultId == self.candidateWiseResultId,
            ElectionCandidate.Model.electionId == self.submission.electionId
        ).all()


Model = TallySheetVersionPRE41Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_41:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    submissionVersion = SubmissionVersion.create(submissionId=tallySheetId)
    candidateWiseResult = CandidateWiseResult.create()

    result = Model(
        tallySheetVersionId=submissionVersion.submissionVersionId,
        candidateWiseResultId=candidateWiseResult.candidateWiseResultId
    )

    db.session.add(result)
    db.session.commit()

    return result

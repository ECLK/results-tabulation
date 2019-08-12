from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof, History, HistoryVersion, Submission

from orm.enums import TallySheetCodeEnum, ProofTypeEnum, SubmissionTypeEnum


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'

    tallySheetId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[tallySheetId])

    electionId = association_proxy("submission", "electionId")
    officeId = association_proxy("submission", "areaId")
    office = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    parentSubmission = association_proxy("submission", "parentSubmission")
    childSubmissions = association_proxy("submission", "childSubmissions")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")


Model = TallySheetModel


def get_by_id(tallySheetId):
    result = Model.query.filter(
        Model.tallySheetId == tallySheetId
    ).one_or_none()

    return result


def get_all(electionId=None, officeId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.submission.electionId == electionId)

    if officeId is not None:
        query = query.filter(Model.submission.areaId == officeId)

    result = get_paginated_query(query).all()

    return result


def create(tallySheetCode, electionId, officeId):
    submission = Submission.create(
        submissionType=SubmissionTypeEnum.TallySheet,
        electionId=electionId,
        areaId=officeId,
        electorateId=None,
        parentSubmissionId=None
    )

    result = Model(
        tallySheetId=submission.submissionId,
        tallySheetCode=tallySheetCode,
    )

    db.session.add(result)
    db.session.commit()

    return result

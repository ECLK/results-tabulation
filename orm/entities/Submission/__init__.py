from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof, History, HistoryVersion, Electorate

from orm.enums import SubmissionTypeEnum, ProofTypeEnum


class SubmissionModel(db.Model):
    __tablename__ = 'submission'
    submissionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submissionType = db.Column(db.Enum(SubmissionTypeEnum), nullable=False)
    parentSubmissionId = db.Column(db.Integer, db.ForeignKey(submissionId), nullable=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=False)
    electorateId = db.Column(db.Integer, db.ForeignKey(Electorate.Model.__table__.c.electorateId), nullable=True)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    submissionProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)
    submissionHistoryId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId), nullable=False)

    parentSubmission = relationship("SubmissionModel", remote_side=[submissionId])
    childSubmissions = relationship("SubmissionModel", foreign_keys=[parentSubmissionId])
    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])
    electorate = relationship(Electorate.Model, foreign_keys=[electorateId])
    submissionProof = relationship(Proof.Model, foreign_keys=[submissionProofId])
    submissionHistory = relationship(History.Model, foreign_keys=[submissionHistoryId])
    latestVersion = relationship("SubmissionVersionModel", foreign_keys=[latestVersionId])
    versions = relationship("SubmissionVersionModel", order_by="desc(SubmissionVersionModel.submissionVersionId)",
                            primaryjoin="SubmissionModel.submissionId==SubmissionVersionModel.submissionId")


Model = SubmissionModel


def get_by_id(submissionId):
    result = Model.query.filter(
        Model.submissionId == submissionId
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


def get_submission_proof_type(submissionType):
    if submissionType is SubmissionTypeEnum.TallySheet:
        return ProofTypeEnum.ManuallyFilledTallySheets
    elif submissionType is SubmissionTypeEnum.Report:
        return ProofTypeEnum.ManuallyFilledReports

    return None


def create(submissionType, electionId, officeId, electorateId=None, parentSubmissionId=None):
    submissionProof = Proof.create(proofType=get_submission_proof_type(submissionType=submissionType))
    submissionHistory = History.create()

    result = Model(
        electionId=electionId,
        submissionType=submissionType,
        officeId=officeId,
        electorateId=electorateId,
        parentSubmissionId=parentSubmissionId,
        submissionProofId=submissionProof.proofId,
        submissionHistoryId=submissionHistory.historyId
    )

    db.session.add(result)
    db.session.commit()

    return result

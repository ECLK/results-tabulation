from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import func

from util import get_paginated_query

from orm.entities import Election, Office, Proof, History, HistoryVersion, Electorate, SubmissionVersion

from orm.enums import SubmissionTypeEnum, ProofTypeEnum


class SubmissionModel(db.Model):
    __tablename__ = 'submission'
    submissionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submissionType = db.Column(db.Enum(SubmissionTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.areaId), nullable=False)
    submissionProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)
    submissionHistoryId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId), nullable=False)

    election = relationship(Election.Model, foreign_keys=[electionId])
    area = relationship(Office.Model, foreign_keys=[areaId])
    submissionProof = relationship(Proof.Model, foreign_keys=[submissionProofId])
    submissionHistory = relationship(History.Model, foreign_keys=[submissionHistoryId])
    versions = relationship("SubmissionVersionModel", order_by="desc(SubmissionVersionModel.submissionVersionId)",
                            primaryjoin="SubmissionModel.submissionId==SubmissionVersionModel.submissionId")

    children = relationship("SubmissionModel", secondary="submission_submission",
                            primaryjoin="SubmissionModel.submissionId==SubmissionChildrenModel.parentSubmissionId",
                            secondaryjoin="SubmissionModel.submissionId==SubmissionChildrenModel.childSubmissionId"
                            )
    parents = relationship("SubmissionModel", secondary="submission_submission",
                           primaryjoin="SubmissionModel.submissionId==SubmissionChildrenModel.childSubmissionId",
                           secondaryjoin="SubmissionModel.submissionId==SubmissionChildrenModel.parentSubmissionId"
                           )

    @hybrid_property
    def latestVersionId(self):
        return db.session.query(
            func.max(SubmissionVersion.Model.submissionVersionId)
        ).filter(
            SubmissionVersion.Model.submissionId == self.submissionId
        ).scalar()

    @hybrid_property
    def latestVersion(self):
        # return db.session.query(func.max("SubmissionVersionModel.submissionVersionId")).scalar()
        SubmissionVersion.Model.query.filter(
            SubmissionVersion.Model.submissionVersionId == self.latestVersionId
        ).one_or_none()

    def __init__(self, submissionType, electionId, areaId):
        submissionProof = Proof.create(proofType=get_submission_proof_type(submissionType=submissionType))
        submissionHistory = History.create()

        super(SubmissionModel, self).__init__(
            electionId=electionId,
            submissionType=submissionType,
            areaId=areaId,
            submissionProofId=submissionProof.proofId,
            submissionHistoryId=submissionHistory.historyId
        )

        db.session.add(self)
        db.session.commit()

    def add_parent(self, parentId):
        db.session.add(SubmissionChildrenModel(parentSubmissionId=parentId, childSubmissionId=self.submissionId))
        db.session.commit()

        return self

    def add_child(self, childId):
        db.session.add(SubmissionChildrenModel(parentSubmissionId=self.submissionId, childSubmissionId=childId))
        db.session.commit()

        return self


class SubmissionChildrenModel(db.Model):
    __tablename__ = 'submission_submission'
    parentSubmissionId = db.Column(db.Integer, db.ForeignKey("submission.submissionId"), primary_key=True)
    childSubmissionId = db.Column(db.Integer, db.ForeignKey("submission.submissionId"), primary_key=True)


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
        query = query.filter(Model.areaId == officeId)

    result = get_paginated_query(query).all()

    return result


def get_submission_proof_type(submissionType):
    if submissionType is SubmissionTypeEnum.TallySheet:
        return ProofTypeEnum.ManuallyFilledTallySheets
    elif submissionType is SubmissionTypeEnum.Report:
        return ProofTypeEnum.ManuallyFilledReports

    return None


def create(submissionType, electionId, areaId):
    result = Model(
        electionId=electionId,
        submissionType=submissionType,
        areaId=areaId
    )

    return result

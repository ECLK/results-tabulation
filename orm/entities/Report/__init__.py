from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, Office, Electorate, Proof, History, Submission
from orm.enums import ReportCodeEnum, ProofTypeEnum, SubmissionTypeEnum

from util import get_paginated_query


class ReportModel(db.Model):
    __tablename__ = 'report'

    reportId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    reportCode = db.Column(db.Enum(ReportCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[reportId])

    electionId = association_proxy("submission", "electionId")
    area = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    parentSubmission = association_proxy("submission", "parentSubmission")
    childSubmissions = association_proxy("submission", "childSubmissions")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")


Model = ReportModel


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


def create(reportCode, electionId, areaId=None, electorateId=None, parentSubmissionId=None):
    submission = Submission.create(
        submissionType=SubmissionTypeEnum.Report,
        electionId=electionId,
        areaId=areaId,
        electorateId=electorateId,
        parentSubmissionId=parentSubmissionId
    )

    result = Model(
        reportId=submission.submissionId,
        reportCode=reportCode,
    )

    db.session.add(result)
    db.session.commit()

    return result

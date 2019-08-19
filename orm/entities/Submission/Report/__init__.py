from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, Office, Electorate, Proof, History, Submission
from orm.entities.SubmissionVersion import ReportVersion
from orm.enums import ReportCodeEnum, ProofTypeEnum, SubmissionTypeEnum

from util import get_paginated_query


class ReportModel(db.Model):
    __tablename__ = 'report'

    reportId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    reportCode = db.Column(db.Enum(ReportCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[reportId])

    electionId = association_proxy("submission", "electionId")
    area = association_proxy("submission", "area")
    areaId = association_proxy("submission", "areaId")
    latestVersionId = association_proxy("submission", "latestVersionId")
    latestVersion = association_proxy("submission", "latestVersion")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")

    def __init__(self, electionId, areaId):
        submission = Submission.create(
            submissionType=SubmissionTypeEnum.Report,
            electionId=electionId,
            areaId=areaId
        )

        super(ReportModel, self).__init__(
            reportId=submission.submissionId
        )

        db.session.add(self)
        db.session.commit()

    @hybrid_property
    def latestVersion(self):
        return ReportVersion.get_by_id(
            reportVersionId=self.latestVersionId
        )

    __mapper_args__ = {
        'polymorphic_on': reportCode
    }


Model = ReportModel


def get_by_id(reportId):
    result = Model.query.filter(
        Model.reportId == reportId
    ).one_or_none()

    return result


def get_all(electionId=None, areaId=None, reportCode=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if areaId is not None:
        query = query.filter(Model.areaId == areaId)

    if reportCode is not None:
        query = query.filter(Model.reportCode == reportCode)

    result = get_paginated_query(query).all()

    return result

# def create(reportCode, electionId, areaId=None, childSubmissionIds=None):
#     result = ReportModel(
#         reportCode=reportCode,
#         electionId=electionId,
#         areaId=areaId,
#         childSubmissionIds=childSubmissionIds
#     )
#
#     return result

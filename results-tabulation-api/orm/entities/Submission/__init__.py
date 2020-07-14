from sqlalchemy.ext.hybrid import hybrid_property
from app import db, cache
from sqlalchemy.orm import relationship
from exception import MethodNotAllowedException
from exception.messages import MESSAGE_CODE_SUBMISSION_IRRELEVANT_VERSION_CANNOT_BE_MAPPED
from orm.entities import Election, Office, Proof, History, SubmissionVersion, Area
from orm.entities.Audit import Stamp
from orm.enums import SubmissionTypeEnum, ProofTypeEnum


class SubmissionModel(db.Model):
    __tablename__ = 'submission'
    submissionId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId), primary_key=True)
    submissionType = db.Column(db.Enum(SubmissionTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.areaId), nullable=False)
    submissionProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    latestStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
    lockedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    lockedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
    submittedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    submittedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
    notifiedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    notifiedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
    releasedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
    releasedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId], lazy='subquery')
    area = relationship(Area.Model, foreign_keys=[areaId], lazy='subquery')
    submissionHistory = relationship(History.Model, foreign_keys=[submissionId])
    latestVersion = relationship("SubmissionVersionModel", foreign_keys=[latestVersionId])
    versions = relationship("SubmissionVersionModel", order_by="desc(SubmissionVersionModel.submissionVersionId)",
                            primaryjoin="SubmissionModel.submissionId==SubmissionVersionModel.submissionId")

    def set_latest_version(self, submissionVersion: SubmissionVersion):
        if submissionVersion is None:
            self.latestVersionId = None
            self.latestStampId = None
        else:
            if submissionVersion.submissionId != self.submissionId:
                raise MethodNotAllowedException(
                    message="%s version is not belongs to the %s (submissionId=%d, submissionVersionId=%d, submissionVersion.submissionId=%d)" % (
                        self.submissionType.name, self.submissionType.name, self.submissionId,
                        submissionVersion.submissionVersionId, submissionVersion.submissionId
                    ),
                    code=MESSAGE_CODE_SUBMISSION_IRRELEVANT_VERSION_CANNOT_BE_MAPPED
                )

            self.latestVersionId = submissionVersion.submissionVersionId
            self.latestStampId = Stamp.create().stampId

        db.session.add(self)
        db.session.flush()

    def __init__(self, submissionType, electionId, areaId):
        submissionProof = Proof.create(proofType=get_submission_proof_type(submissionType=submissionType))
        submissionHistory = History.create()

        super(SubmissionModel, self).__init__(
            submissionId=submissionHistory.historyId,
            electionId=electionId,
            submissionType=submissionType,
            areaId=areaId,
            submissionProofId=submissionProof.proofId
        )

        db.session.add(self)
        db.session.flush()


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

    return query


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

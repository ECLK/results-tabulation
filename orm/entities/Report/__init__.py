from app import db
from sqlalchemy.orm import relationship
from orm.entities import Election, Office, Electorate, Proof, History
from orm.enums import ReportCodeEnum, ProofTypeEnum

from util import get_paginated_query


class ReportModel(db.Model):
    __tablename__ = 'report'
    reportId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reportCode = db.Column(db.Enum(ReportCodeEnum), nullable=False)
    parentReportId = db.Column(db.Integer, db.ForeignKey(reportId), nullable=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=True)
    electorateId = db.Column(db.Integer, db.ForeignKey(Electorate.Model.__table__.c.electorateId), nullable=True)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("reportVersion.reportVersionId"), nullable=True)
    reportProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)
    reportHistoryId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId), nullable=False)

    parentOffice = relationship("ReportModel", remote_side=[reportId])
    childOffices = relationship("ReportModel", foreign_keys=[parentReportId])
    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])
    electorate = relationship(Electorate.Model, foreign_keys=[electorateId])
    reportProof = relationship(Proof.Model, foreign_keys=[reportProofId])
    reportHistory = relationship(History.Model, foreign_keys=[reportHistoryId])
    latestVersion = relationship("ReportVersionModel", foreign_keys=[latestVersionId])
    versions = relationship("ReportVersionModel", order_by="desc(ReportVersionModel.reportVersionId)",
                            primaryjoin="ReportModel.reportId==ReportVersionModel.reportId")


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


def create(reportCode, electionId, officeId=None, electorateId=None, parentReportId=None):
    reportProof = Proof.create(proofType=ProofTypeEnum.ManuallyFilledReports)
    reportHistory = History.create()

    result = Model(
        reportCode=reportCode,
        parentReportId=parentReportId,
        electionId=electionId,
        officeId=officeId,
        electorateId=electorateId,
        reportProofId=reportProof.proofId,
        reportHistoryId=reportHistory.historyId
    )

    db.session.add(result)
    db.session.commit()

    return result

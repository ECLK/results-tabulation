from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship
from orm.entities.Election import ElectionModel
from orm.entities.Area.Electorate import ElectoralDistrict, PollingDistrict, PollingDivision
from orm.entities.Area.Office import Area
from orm.entities import Candidate


class StatusPRE34Model(db.Model):
    __tablename__ = 'dashboard_status_PRE_34'

    recordId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voteType = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(ElectionModel.electionId), autoincrement=True)
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    countingCentreId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.CandidateModel.candidateId), autoincrement=True)
    secondPreferenceCount = db.Column(db.Integer, nullable=False)
    thirdPreferenceCount = db.Column(db.Integer, nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    electoralDistrict = relationship("ElectoralDistrictModel", foreign_keys=[electoralDistrictId])
    pollingDivision = relationship("PollingDivisionModel", foreign_keys=[pollingDivisionId])

    def __init__(self, electionId, electoralDistrictId, pollingDivisionId, countingCentreId, secondPreferenceCount
                 , thirdPreferenceCount, candidateId, voteType="NonPostal", status="Pending"):
        super(StatusPRE34Model, self).__init__(
            voteType=voteType,
            status=status,
            electionId=electionId,
            electoralDistrictId=electoralDistrictId,
            pollingDivisionId=pollingDivisionId,
            countingCentreId=countingCentreId,
            secondPreferenceCount=secondPreferenceCount,
            thirdPreferenceCount=thirdPreferenceCount,
            candidateId=candidateId
        )

        db.session.add(self)
        db.session.flush()


Model = StatusPRE34Model


def create(electionId, electoralDistrictId, pollingDivisionId, countingCentreId, secondPreferenceCount
           , thirdPreferenceCount, candidateId, voteType="NonPostal", status="Pending"):
    result = Model(
        voteType=voteType,
        status=status,
        electionId=electionId,
        electoralDistrictId=electoralDistrictId,
        pollingDivisionId=pollingDivisionId,
        countingCentreId=countingCentreId,
        secondPreferenceCount=secondPreferenceCount,
        thirdPreferenceCount=thirdPreferenceCount,
        candidateId=candidateId
    )

    return result


def get_status_record(electionId, electoralDistrictId, pollingDivisionId, countingCentreId, candidateId,
                      pollingStationId=None):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.electoralDistrictId == electoralDistrictId,
        Model.pollingDivisionId == pollingDivisionId,
        Model.countingCentreId == countingCentreId,
        Model.pollingStationId == pollingStationId,
        Model.candidateId == candidateId
    ).one_or_none()

    return result


def get_status_records(electionId, countingCentreId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.countingCentreId == countingCentreId
    ).all()

    return result

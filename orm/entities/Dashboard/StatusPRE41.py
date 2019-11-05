from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship
from orm.entities.Election import ElectionModel
from orm.entities.Area.Electorate import ElectoralDistrict, PollingDistrict, PollingDivision
from orm.entities.Area.Office import Area
from orm.entities import Candidate


class StatusPRE41Model(db.Model):
    __tablename__ = 'dashboard_status_PRE_41'

    recordId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voteType = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(ElectionModel.electionId), autoincrement=True)
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    countingCentreId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    pollingStationId = db.Column(db.Integer, db.ForeignKey(Area.AreaModel.areaId), autoincrement=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.CandidateModel.candidateId), autoincrement=True)
    voteCount = db.Column(db.Integer, nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    electoralDistrict = relationship("ElectoralDistrictModel", foreign_keys=[electoralDistrictId])
    pollingDivision = relationship("PollingDivisionModel", foreign_keys=[pollingDivisionId])

    def __init__(self, electionId, electoralDistrictId, pollingDivisionId, countingCentreId,
                 pollingStationId, candidateId, voteType="NonPostal", status="Pending", voteCount=0):
        super(StatusPRE41Model, self).__init__(
            voteType=voteType,
            status=status,
            electionId=electionId,
            electoralDistrictId=electoralDistrictId,
            pollingDivisionId=pollingDivisionId,
            countingCentreId=countingCentreId,
            pollingStationId=pollingStationId,
            candidateId=candidateId,
            voteCount=voteCount
        )

        db.session.add(self)
        db.session.flush()


Model = StatusPRE41Model


def create(electionId, electoralDistrictId, pollingDivisionId, countingCentreId,
           pollingStationId, candidateId, voteType="NonPostal", status="Pending", voteCount=0):
    result = Model(
        voteType=voteType,
        status=status,
        electionId=electionId,
        electoralDistrictId=electoralDistrictId,
        pollingDivisionId=pollingDivisionId,
        countingCentreId=countingCentreId,
        pollingStationId=pollingStationId,
        candidateId=candidateId,
        voteCount=voteCount
    )

    return result

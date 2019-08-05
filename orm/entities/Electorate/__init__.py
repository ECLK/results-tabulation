from app import db
from sqlalchemy.orm import relationship
from orm.enums import ElectorateTypeEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query


class ElectorateModel(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateName = db.Column(db.String(100), nullable=False)
    electorateType = db.Column(db.Enum(ElectorateTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    parentElectorateId = db.Column(db.Integer, db.ForeignKey(electorateId), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    parentElectorate = relationship("ElectorateModel", remote_side=[electorateId])
    childElectorates = relationship("ElectorateModel", foreign_keys=[parentElectorateId])
    pollingStations = relationship("PollingStationModel")

    @hybrid_property
    def allPollingStations(self):
        result = self.pollingStations
        if self.childElectorates is not None:
            for childElectorate in self.childElectorates:
                result = result + childElectorate.allPollingStations

        return result

    __mapper_args__ = {
        'polymorphic_on': electorateType
    }


Model = ElectorateModel


def create(electorateName, electorateType, electionId, parentElectorateId=None):
    result = Model(
        electorateName=electorateName,
        electorateType=electorateType,
        electionId=electionId,
        parentElectorateId=parentElectorateId
    )
    db.session.add(result)
    db.session.commit()

    return result


def get_all():
    query = Model.query
    result = query.all()

    return result

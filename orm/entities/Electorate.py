from config import db
from sqlalchemy.orm import relationship
from orm.enums import ElectorateTypeEnum
from orm.entities import Election


class ElectorateModel(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateName = db.Column(db.String(100), nullable=False)
    electorateType = db.Column(db.Enum(ElectorateTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    parentElectorateId = db.Column(db.Integer, db.ForeignKey(electorateId), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    parentElectorate = relationship("ElectorateModel", foreign_keys=[parentElectorateId])


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

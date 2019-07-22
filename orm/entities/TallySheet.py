from config import db
from sqlalchemy.orm import relationship

from orm.entities import Office, Election


class Model(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=False)


    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])



def create(code, electionId, officeId):
    result = Model(
        electionId=electionId,
        code=code,
        officeId=officeId
    )

    db.session.add(result)
    db.session.commit()

    return result

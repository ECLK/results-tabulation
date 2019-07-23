from config import db
from sqlalchemy.orm import relationship

from orm.entities import Office, Election

print("#####", Election.Model.electionId)
print("#####", Election.Model.__table__.c.electionId)
print("#####", Election.Model.__tablename__)
print("#####", Election.Model.electionId._parententity)
print("#####", Election.Model.electionId._parentmapper)


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=False)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"), nullable=True,
                                post_update=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])
    latestVersion = relationship("TallySheetVersionModel", foreign_keys=[latestVersionId], post_update=True)


Model = TallySheetModel


def create(code, electionId, officeId):
    result = Model(
        electionId=electionId,
        code=code,
        officeId=officeId
    )

    db.session.add(result)
    db.session.commit()

    return result

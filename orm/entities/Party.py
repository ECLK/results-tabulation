from app import db
from sqlalchemy.orm import relationship
from orm.entities.IO.File import Image


class PartyModel(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partyName = db.Column(db.String(100), nullable=False)
    partySymbolFileId = db.Column(db.Integer, db.ForeignKey(Image.Model.__table__.c.fileId), nullable=True)

    partySymbol = relationship(Image.Model)


Model = PartyModel


def get_by_id(partyId):
    result = Model.query.filter(
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(partyName, partySymbolFileSource=None):
    if partySymbolFileSource is not None:
        partySymbolFile = Image.create(partySymbolFileSource)
        result = Model(
            partyName=partyName,
            partySymbolFileId=partySymbolFile.fileId
        )
    else:
        result = Model(
            partyName=partyName
        )

    db.session.add(result)
    db.session.commit()

    return result

from app import db
from sqlalchemy.orm import relationship
from orm.entities.IO.File import Image


class PartyModel(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partyName = db.Column(db.String(100), nullable=False)
    partySymbol = db.Column(db.String(100), nullable=False)
    partyAbbreviation = db.Column(db.String(50), nullable=True)
    partySymbolFileId = db.Column(db.Integer, db.ForeignKey(Image.Model.__table__.c.fileId), nullable=True)

    partySymbolFile = relationship(Image.Model)

    def __init__(self, partyName, partySymbol, partyAbbreviation, partySymbolFileSource=None,):
        if partySymbolFileSource is not None:
            partySymbolFile = Image.create(partySymbolFileSource)
            super(PartyModel, self).__init__(
                partyName=partyName,
                partySymbol=partySymbol,
                partySymbolFileId=partySymbolFile.fileId,
                partyAbbreviation = partyAbbreviation
            )
        else:
            super(PartyModel, self).__init__(
                partyName=partyName,
                partySymbol=partySymbol,
                partyAbbreviation=partyAbbreviation
            )

        db.session.add(self)
        db.session.flush()


Model = PartyModel


def get_by_id(partyId):
    result = Model.query.filter(
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(partyName, partySymbol, partyAbbreviation, partySymbolFileSource=None):
    result = Model(
        partyName=partyName,
        partySymbol=partySymbol,
        partySymbolFileSource=partySymbolFileSource,
        partyAbbreviation=partyAbbreviation
    )

    return result

from app import db
from orm.entities.Meta import MetaData
from sqlalchemy.orm import relationship


class MetaModel(db.Model):
    __tablename__ = 'meta'

    metaId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    metaDataList = relationship(MetaData.Model)

    @classmethod
    def create(cls, metaDataDict):
        meta = MetaModel()
        for meta_key in metaDataDict:
            meta_value = metaDataDict[meta_key]
            MetaData.create(metaId=meta.metaId, metaDataKey=meta_key, metaDataValue=meta_value)

        return meta

    def __init__(self):
        db.session.add(self)
        db.session.flush()


Model = MetaModel

create = MetaModel.create

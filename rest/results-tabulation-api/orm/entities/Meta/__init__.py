from app import db
from orm.entities.Meta import MetaData
from sqlalchemy.orm import relationship


class MetaModel(db.Model):
    __tablename__ = 'meta'

    metaId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    metaDataList = relationship(MetaData.Model)

    @classmethod
    def create(cls, metaDataDict=None):
        meta = MetaModel()
        if metaDataDict:
            for meta_key in metaDataDict:
                meta_value = metaDataDict[meta_key]
                meta.add_meta_data(metaDataKey=meta_key, metaDataValue=meta_value)

        return meta

    def add_meta_data(self, metaDataKey, metaDataValue):
        return MetaData.create(metaId=self.metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)

    def get_meta_data(self, metaDataKey):
        meta_data = db.session.query(
            MetaData.Model.metaDataValue
        ).filter(
            MetaData.Model.metaId == self.metaId,
            MetaData.Model.metaDataKey == metaDataKey
        ).one_or_none()

        if meta_data:
            return meta_data.metaDataValue
        else:
            return None

    def __init__(self):
        db.session.add(self)
        db.session.flush()


Model = MetaModel

create = MetaModel.create

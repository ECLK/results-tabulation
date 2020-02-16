from app import db
from orm.entities import Meta


class MetaDataModel(db.Model):
    __tablename__ = 'metaData'

    metaDataId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    metaId = db.Column(db.Integer, db.ForeignKey("meta.metaId"), nullable=False)
    metaDataKey = db.Column(db.String(100), nullable=False)
    metaDataValue = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('metaId', 'metaDataKey', name='MetaDataModelUK'),
    )

    @classmethod
    def create(cls, metaId, metaDataKey, metaDataValue):
        return MetaDataModel(metaId=metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)

    def __init__(self, metaId, metaDataKey, metaDataValue):
        super(MetaDataModel, self).__init__(metaId=metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)
        db.session.add(self)
        db.session.flush()


Model = MetaDataModel

create = MetaDataModel.create

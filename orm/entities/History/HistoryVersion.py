from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities import History
from orm.entities.Audit import Stamp


class HistoryVersionModel(db.Model):
    __tablename__ = 'history_version'
    historyVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    historyId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId))
    historyStampId = db.Column(db.Integer, db.ForeignKey(Stamp.Model.__table__.c.stampId), nullable=False)

    historyStamp = relationship(Stamp.Model, foreign_keys=[historyStampId])
    createdBy = association_proxy("historyStamp", "createdBy")
    createdAt = association_proxy("historyStamp", "createdAt")

    def __init__(self, historyId):
        history_stamp = Stamp.create()

        super(HistoryVersionModel, self).__init__(
            historyId=historyId,
            historyStampId=history_stamp.stampId
        )

        db.session.add(self)
        db.session.flush()


Model = HistoryVersionModel


def create(historyId):
    result = Model(historyId=historyId)

    return result

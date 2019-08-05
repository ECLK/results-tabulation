from datetime import datetime
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities import History


class HistoryVersionModel(db.Model):
    __tablename__ = 'history_version'
    historyVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    historyId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId))
    createdBy = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


Model = HistoryVersionModel

from datetime import datetime
from app import db
from sqlalchemy.orm import relationship


class HistoryModel(db.Model):
    __tablename__ = 'history'
    historyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    versions = relationship("HistoryVersionModel")


Model = HistoryModel


def create():
    result = Model()

    db.session.add(result)
    db.session.commit()

    return result

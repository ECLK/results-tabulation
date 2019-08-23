from datetime import datetime
from app import db
from sqlalchemy.orm import relationship


class HistoryModel(db.Model):
    __tablename__ = 'history'
    historyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    versions = relationship("HistoryVersionModel")

    def __init__(self):
        super(HistoryModel, self).__init__()

        db.session.add(self)
        db.session.commit()


Model = HistoryModel


def create():
    result = Model()

    return result

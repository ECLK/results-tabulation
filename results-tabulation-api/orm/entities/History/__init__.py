from datetime import datetime
from app import db
from sqlalchemy.orm import relationship


class HistoryModel(db.Model):
    __tablename__ = 'history'
    historyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    versions = relationship("HistoryVersionModel")

    @classmethod
    def create(cls):
        history = cls()
        db.session.add(history)
        db.session.flush()

        return history


Model = HistoryModel
create = Model.create

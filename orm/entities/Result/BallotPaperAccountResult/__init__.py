from sqlalchemy.orm import relationship

from app import db


class BallotPaperAccountResultModel(db.Model):
    __tablename__ = 'ballotPaperAccountResult'
    ballotPaperAccountResultId = db.Column(db.Integer, primary_key=True, autoincrement=True)


Model = BallotPaperAccountResultModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result

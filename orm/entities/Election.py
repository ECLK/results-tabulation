from config import db


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


Model = ElectionModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result

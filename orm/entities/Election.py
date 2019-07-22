from config import db


class Model(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result

from config import db


class UserModel(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)


Model = UserModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result

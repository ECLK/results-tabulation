from config import db


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)

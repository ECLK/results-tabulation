from datetime import datetime
from app import db
from auth import get_user_name, get_ip


class Stamp(db.Model):
    __tablename__ = 'stamp'
    stampId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100), default=get_ip, nullable=False)
    createdBy = db.Column(db.String(100), default=get_user_name, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now, nullable=False)


Model = Stamp


def create():
    result = Stamp()

    db.session.add(result)
    db.session.flush()

    return result

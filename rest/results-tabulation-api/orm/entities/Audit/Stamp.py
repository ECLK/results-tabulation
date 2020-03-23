from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from auth import get_user_name, get_ip
from orm.entities.Audit import Barcode


class Stamp(db.Model):
    __tablename__ = 'stamp'
    stampId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100), default=get_ip, nullable=False)
    createdBy = db.Column(db.String(100), default=get_user_name, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now, nullable=False)
    barcodeId = db.Column(db.Integer, db.ForeignKey(Barcode.Model.__table__.c.barcodeId), nullable=False)

    barcode = relationship(Barcode.Model, foreign_keys=[barcodeId])

    barcodeString = association_proxy("barcode", "barcodeString")

    @classmethod
    def create(cls):
        barcode = Barcode.create()
        stamp = cls(barcodeId=barcode.barcodeId)

        db.session.add(stamp)
        db.session.flush()

        return stamp


Model = Stamp
create = Model.create

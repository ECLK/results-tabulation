from app import db
import barcode

EAN = barcode.get_barcode_class('ean')
BARCODE_LENGTH = 12


class BarcodeModel(db.Model):
    __tablename__ = 'barcode'
    barcodeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcodeString = db.Column(db.String(13), nullable=True)


Model = BarcodeModel


def _get_barcode_string(num):
    num_str = str(num)
    for i in range(12 - len(num_str)):
        num_str = "0" + num_str
    return num_str


def create(barcodeString):
    barcode = BarcodeModel()
    db.session.add(barcode)
    db.session.flush()

    barcode.barcodeString = EAN(_get_barcode_string(barcode.barcodeId))

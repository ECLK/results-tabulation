from app import db

BARCODE_LENGTH = 13


class BarcodeModel(db.Model):
    __tablename__ = 'barcode'
    barcodeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcodeString = db.Column(db.String(13), nullable=True)


Model = BarcodeModel


def _get_barcode_string(num):
    num_str = str(num)
    for i in range(BARCODE_LENGTH - len(num_str)):
        num_str = "0" + num_str
    return num_str


def create():
    barcode = BarcodeModel()
    db.session.add(barcode)
    db.session.flush()

    barcode.barcodeString = _get_barcode_string(barcode.barcodeId)
    db.session.flush()

    return barcode

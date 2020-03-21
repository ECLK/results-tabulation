from app import db

BARCODE_LENGTH = 13


class BarcodeModel(db.Model):
    __tablename__ = 'barcode'
    barcodeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcodeString = db.Column(db.String(13), nullable=True)

    @classmethod
    def _get_barcode_string(cls, num):
        num_str = str(num)
        for i in range(BARCODE_LENGTH - len(num_str)):
            num_str = "0" + num_str
        return num_str

    @classmethod
    def create(cls):
        barcode = cls()
        db.session.add(barcode)
        db.session.flush()

        barcode.barcodeString = cls._get_barcode_string(barcode.barcodeId)
        db.session.flush()

        return barcode


Model = BarcodeModel
create = Model.create

from config import db
from models import InvoiceStationaryItemModel as Model


def get_all(invoiceId):
    result = Model.query.filter(Model.invoiceId == invoiceId).all()

    return result


def create(invoiceId, body):
    result = Model(
        invoiceId=invoiceId,
        stationaryItemId=body["stationaryItemId"]
    )

    db.session.add(result)
    db.session.commit()

    return result

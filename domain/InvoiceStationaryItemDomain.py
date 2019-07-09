from config import db
from models import InvoiceStationaryItemModel as Model


def get_all(invoiceId):
    result = Model.query.filter(Model.invoiceId == invoiceId).all()

    return result


def create(invoiceId, stationaryItemId):
    result = Model(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result

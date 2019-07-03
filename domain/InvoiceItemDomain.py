from config import db
from models import InvoiceItemModel as Model


def get_all():
    result = Model.query.all()

    return result


def create():
    result = Model()

    db.session.add(result)
    db.session.commit()

    return result

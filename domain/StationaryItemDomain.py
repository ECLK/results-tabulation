from config import db
from util import Auth
from datetime import datetime

from models import StationaryItemModel as Model
from domain import InvoiceStationaryItemDomain
from exception import NotFoundException


def get_all():
    result = Model.query.all()

    return result


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def create(electionId, stationaryItemType):
    result = Model(
        electionId=electionId,
        stationaryItemType=stationaryItemType
    )

    db.session.add(result)
    db.session.commit()

    return result


def is_locked(stationaryItemId):
    entry = get_by_id(stationaryItemId)

    if entry is None:
        raise NotFoundException("Stationary Item Not Found (stationaryItemId=%d) " % stationaryItemId)
    else:
        return entry.locked

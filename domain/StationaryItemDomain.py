from config import db
from util import Auth
from datetime import datetime

from models import StationaryItemModel as Model


def get_all():
    result = Model.query.all()

    return result


def create(electionId, stationaryItemType):
    result = Model(
        electionId=electionId,
        stationaryItemType=stationaryItemType
    )

    db.session.add(result)
    db.session.commit()

    return result

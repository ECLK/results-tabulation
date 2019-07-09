from config import db
from models import BallotBoxModel as Model
from domain import StationaryItemDomain


def get_all():
    result = Model.query.all()

    return result


def create(ballotBoxId):
    stationary_item = StationaryItemDomain.create()
    result = Model(
        ballotBoxId=ballotBoxId,
        stationaryItemId=stationary_item.stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result

from config import db
from models import BallotModel as Model
from domain import StationaryItemDomain


def get_all():
    result = Model.query.all()

    return result


def create(body):
    stationary_item = StationaryItemDomain.create()
    result = Model(
        ballotId=body["ballotId"],
        stationaryItemId=stationary_item.stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result

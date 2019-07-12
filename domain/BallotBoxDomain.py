from config import db
from models import StationaryItemTypeEnum
from domain import StationaryItemDomain

from models import BallotBoxModel as Model


def get_all():
    result = Model.query.all()

    return result


def create(electionId, ballotBoxId):
    stationary_item = StationaryItemDomain.create(
        electionId=electionId,
        stationaryItemType=StationaryItemTypeEnum.BallotBox
    )

    result = Model(
        electionId=electionId,
        ballotBoxId=ballotBoxId,
        stationaryItemId=stationary_item.stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result

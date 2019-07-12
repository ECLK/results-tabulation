from config import db
from models import BallotModel as Model
from models import StationaryItemTypeEnum
from domain import StationaryItemDomain


def get_all():
    result = Model.query.all()

    return result


def create(electionId, ballotId):
    stationary_item = StationaryItemDomain.create(
        electionId=electionId,
        stationaryItemType=StationaryItemTypeEnum.Ballot
    )

    result = Model(
        electionId=electionId,
        ballotId=ballotId,
        stationaryItemId=stationary_item.stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result

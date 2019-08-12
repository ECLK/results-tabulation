from app import db
from sqlalchemy.orm import relationship
from orm.entities import Electorate, Office
from orm.enums import OfficeTypeEnum, AreaTypeEnum
from util import get_paginated_query


class PollingStationModel(Office.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.PollingStation
    }


Model = PollingStationModel


def create(officeName, electionId, electorateId, parentOfficeId=None):
    result = Model(
        officeName=officeName,
        electionId=electionId,
        parentOfficeId=parentOfficeId,
        electorateId=electorateId
    )
    db.session.add(result)
    db.session.commit()

    return result


def get_all():
    query = Model.query
    result = get_paginated_query(query).all()

    return result

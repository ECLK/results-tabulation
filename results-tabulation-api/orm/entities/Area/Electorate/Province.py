from orm.entities import Electorate
from orm.enums import AreaTypeEnum


class ProvinceModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Province
    }


Model = ProvinceModel


def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result


def get_by_id(provinceId):
    result = Model.query.filter(
        Model.electorateId == provinceId
    ).one_or_none()

    return result


def create(electorateName, electionId):
    result = Model(
        electorateName=electorateName,
        electionId=electionId
    )

    return result

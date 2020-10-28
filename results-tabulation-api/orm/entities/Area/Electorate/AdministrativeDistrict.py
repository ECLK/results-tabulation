from orm.entities.Area import Electorate
from orm.enums import AreaTypeEnum


class AdministrativeDistrictModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.AdministrativeDistrict
    }


Model = AdministrativeDistrictModel


def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result


def get_by_id(administrativeDistrictId):
    result = Model.query.filter(
        Model.electorateId == administrativeDistrictId
    ).one_or_none()

    return result


def create(electorateName, electionId):
    result = Model(
        electorateName=electorateName,
        electionId=electionId
    )

    return result

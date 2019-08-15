from app import db
from orm.entities.Area import Electorate
from orm.entities.Area.Electorate import Province
from orm.enums import ElectorateTypeEnum, AreaTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class AdministrativeDistrictModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.AdministrativeDistrict
    }

    province = synonym("parentElectorate")
    country = association_proxy("parentElectorate", "country")


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

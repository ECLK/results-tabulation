from app import db
from orm.entities.Area import Electorate
from orm.enums import ElectorateTypeEnum, AreaTypeEnum
from sqlalchemy.ext.associationproxy import association_proxy


class CountryModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Country
    }


Model = CountryModel

def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result

def get_by_id(countryId):
    result = Model.query.filter(
        Model.electorateId == countryId
    ).one_or_none()

    return result



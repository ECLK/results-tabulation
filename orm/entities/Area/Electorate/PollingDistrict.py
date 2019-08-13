from app import db
from orm.entities.Area import Electorate
from orm.entities.Area.Electorate import PollingDivision
from orm.enums import AreaTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import synonym
from sqlalchemy.ext.associationproxy import association_proxy


class PollingDistrictModel(Electorate.Model):
    pollingDivision = synonym("parentElectorate")
    electoralDistrict = association_proxy("parentElectorate", "electoralDistrict")
    country = association_proxy("electoralDistrict", "country")

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.PollingDistrict
    }


Model = PollingDistrictModel


def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result


def get_by_id(pollingDistrictId):
    result = Model.query.filter(
        Model.electorateId == pollingDistrictId
    ).one_or_none()

    return result

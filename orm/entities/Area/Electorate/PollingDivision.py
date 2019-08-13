from app import db
from orm.entities import Electorate
from orm.entities.Area.Electorate import ElectoralDistrict
from orm.enums import ElectorateTypeEnum, AreaTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class PollingDivisionModel(Electorate.Model):
    electoralDistrict = synonym("parentElectorate")
    country = association_proxy("parentElectorate", "country")

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.PollingDivision
    }


Model = PollingDivisionModel


def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result


def get_by_id(pollingDivisionId):
    result = Model.query.filter(
        Model.electorateId == pollingDivisionId
    ).one_or_none()

    return result

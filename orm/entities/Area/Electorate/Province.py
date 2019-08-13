from app import db
from orm.entities import Electorate
from orm.entities.Area.Electorate import Country
from orm.enums import ElectorateTypeEnum, AreaTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym


class ProvinceModel(Electorate.Model):
    # parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorateId"), nullable=True)

    country = synonym("parentElectorate")

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

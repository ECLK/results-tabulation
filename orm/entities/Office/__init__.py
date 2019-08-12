from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship, synonym
from orm.enums import OfficeTypeEnum, ElectorateTypeEnum, AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election, Electorate, Area
from sqlalchemy.ext.hybrid import hybrid_property

from util import get_paginated_query


class OfficeModel(Area.Model):
    # __tablename__ = 'office'

    officeId = synonym("areaId")
    officeType = synonym("areaType")
    officeName = synonym("areaName")

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Office,
        'polymorphic_on': "areaType"
    }


Model = OfficeModel


def create(officeName, officeType, electionId, parentOfficeId=None):
    result = Model(
        areaName=officeName,
        areaType=officeType,
        electionId=electionId,
        parentAreaId=parentOfficeId
    )

    # result = Model(
    #     officeId=area.areaId,
    #     officeType=officeType
    # )

    db.session.add(result)
    db.session.commit()

    return result


def get_all(electionId=None, officeName=None, parentOfficeId=None, officeType=None):
    query = Model.query

    if officeName is not None:
        query = query.filter(Model.officeName.like(officeName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    # if officeType is not None:
    #     query = query.filter(Model.officeType == officeType)
    # else:
    #     query = query.filter(Model.parentOfficeId == parentOfficeId)

    result = get_paginated_query(query).all()

    return result

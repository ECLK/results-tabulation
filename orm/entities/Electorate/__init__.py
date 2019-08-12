from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship, synonym
from orm.enums import ElectorateTypeEnum, AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election, Area
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query


class ElectorateModel(Area.Model):
    # __tablename__ = 'electorate'

    electorateId = synonym("areaId")
    electorateName = synonym("areaName")
    electorateType = synonym("areaType")

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Electorate,
        'polymorphic_on': "areaType"
    }


Model = ElectorateModel


def create(electorateName, electorateType, electionId, parentElectorateId=None):
    result = Model(
        areaName=electorateName,
        areaType=electorateType,
        electionId=electionId,
        parentAreaId=parentElectorateId
    )

    db.session.add(result)
    db.session.commit()

    return result


def get_all():
    query = Model.query
    result = query.all()

    return result

from app import db
from sqlalchemy.orm import relationship
from orm.enums import AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query


class AreaModel(db.Model):
    __tablename__ = 'area'
    areaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column(db.String(100), nullable=False)
    areaType = db.Column(db.Enum(AreaTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    # parentAreaId = db.Column(db.Integer, db.ForeignKey(areaId), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    # parentArea = relationship("AreaModel", remote_side=[areaId])
    # childAreas = relationship("AreaModel", foreign_keys=[parentAreaId])
    # pollingStations = relationship("PollingStationModel")

    # this relationship is used for persistence
    children = relationship("AreaModel", secondary="area_area",
                            primaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId",
                            secondaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId"
                            )
    parents = relationship("AreaModel", secondary="area_area",
                           primaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId",
                           secondaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId"
                           )

    def __init__(self, areaName, areaType, electionId, parentAreaId=None):
        super(AreaModel, self).__init__(
            areaName=areaName,
            areaType=areaType,
            electionId=electionId
        )
        db.session.add(self)
        db.session.commit()

        if parentAreaId is not None:
            # TODO validate circular dependencies.
            areaParent = AreaAreaModel(parentAreaId=parentAreaId, childAreaId=self.areaId)
            db.session.add(areaParent)
            db.session.commit()

    # @hybrid_property
    # def pollingStations(self):
    #     result = []
    #     if self.childAreas is not None:
    #         for childArea in self.childAreas:
    #             result = result + childArea.allPollingStations
    #
    #     return result

    __mapper_args__ = {
        'polymorphic_on': areaType
    }


Model = AreaModel


def get_child_areas(area, areaType, visitedAreas=None):
    result = []
    if area.childAreas is not None:
        for childArea in area.childAreas:
            result = result + childArea.allPollingStations

    return result


class AreaAreaModel(db.Model):
    __tablename__ = 'area_area'
    parentAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)
    childAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)


def create(areaName, areaType, electionId, parentAreaId=None):
    area = Model(
        areaName=areaName,
        areaType=areaType,
        electionId=electionId,
        # parentAreaId=parentAreaId
    )
    db.session.add(area)
    db.session.commit()

    if parentAreaId is not None:
        # TODO validate circular dependencies.
        areaParent = AreaAreaModel(parentAreaId=parentAreaId, childAreaId=area.areaId)
        db.session.add(areaParent)
        db.session.commit()

    return area


def get_all():
    query = Model.query
    result = query.all()

    return result

from app import db
from sqlalchemy.orm import relationship
from orm.enums import AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query, get_array


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

    def __init__(self, areaName, areaType, electionId):
        super(AreaModel, self).__init__(
            areaName=areaName,
            areaType=areaType,
            electionId=electionId
        )
        db.session.add(self)
        db.session.commit()

    def add_parent(self, parentId):
        areaParent = AreaAreaModel(parentAreaId=parentId, childAreaId=self.areaId)
        db.session.add(areaParent)
        db.session.commit()

        return self

    def add_child(self, childId):
        areaParent = AreaAreaModel(parentAreaId=self.areaId, childAreaId=childId)
        db.session.add(areaParent)
        db.session.commit()

        return self

    @hybrid_property
    def pollingStations(self):
        #return []
        return get_child_areas(self, AreaTypeEnum.PollingStation)

    __mapper_args__ = {
        'polymorphic_on': areaType
    }


class AreaAreaModel(db.Model):
    __tablename__ = 'area_area'
    parentAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)
    childAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)


Model = AreaModel


def get_child_areas(area, areaType, visitedAreas=[]):
    result = []
    if area.children is not None:
        print("############ 1 ", result)
        for child in area.children:
            print("############ 2 ", result)
            if child.areaId not in visitedAreas:
                print("############ 3 ", child.areaType)
                visitedAreas.append(child.areaId)
                if child.areaType is areaType:
                    result.append(child)
                    print("############ 4 ", result)
                else:
                    result = result + get_child_areas(child, areaType, visitedAreas=visitedAreas)
                    print("############ 5 ", result)

    return result


def create(areaName, areaType, electionId):
    area = Model(
        areaName=areaName,
        areaType=areaType,
        electionId=electionId
    )

    return area


def get_all():
    query = Model.query
    result = query.all()

    return result

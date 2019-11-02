from orm.entities.Area import Electorate
from orm.enums import AreaTypeEnum
from sqlalchemy.orm import synonym


class ElectoralDistrictModel(Electorate.Model):
    country = synonym("parentElectorate")
    #
    # def add_parent(self, parentId):
    #     super(ElectoralDistrictModel, self).add_child(parentId)
    #
    # def add_child(self, childId):
    #     super(ElectoralDistrictModel, self).add_child(childId)

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.ElectoralDistrict
    }


Model = ElectoralDistrictModel


def get_all(electorateName=None, electionId=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    result = query.all()

    return result


def get_by_id(electoralDistrictId):
    result = Model.query.filter(
        Model.electorateId == electoralDistrictId
    ).one_or_none()

    return result


def create(electorateName, electionId):
    result = Model(
        electorateName=electorateName,
        electionId=electionId
    )

    return result

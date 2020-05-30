from sqlalchemy.orm import synonym
from orm.enums import AreaTypeEnum
from orm.entities import Area


class ElectorateModel(Area.Model):
    electorateId = synonym("areaId")
    electorateName = synonym("areaName")
    electorateType = synonym("areaType")

    def __init__(self, electorateName, electionId):
        super(ElectorateModel, self).__init__(
            areaName=electorateName,
            electionId=electionId
        )

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Electorate,
        'polymorphic_on': "areaType"
    }


Model = ElectorateModel


def create(electorateName, electionId):
    result = Model(
        electorateName=electorateName,
        electionId=electionId
    )

    return result


def get_all(electorateName=None, electionId=None, parentElectorateId=None, electorateType=None):
    query = Model.query.join(
        Area.AreaAreaModel,
        Model.areaId == Area.AreaAreaModel.childAreaId,
        isouter=True
    )

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if electorateType is not None:
        query = query.filter(Model.areaType == electorateType)

    if parentElectorateId is not None:
        query = query.filter(Area.AreaAreaModel.parentAreaId == parentElectorateId)

    result = query.all()

    return result

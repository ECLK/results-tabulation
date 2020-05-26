from sqlalchemy.orm import synonym
from orm.enums import AreaTypeEnum
from orm.entities import Area


class OfficeModel(Area.Model):
    officeId = synonym("areaId")
    officeType = synonym("areaType")
    officeName = synonym("areaName")

    def __init__(self, officeName, electionId):
        super(OfficeModel, self).__init__(
            areaName=officeName,
            electionId=electionId
        )

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Office,
        'polymorphic_on': "areaType"
    }


Model = OfficeModel


def create(officeName, officeType, electionId):
    result = Model(
        officeName=officeName,
        officeType=officeType,
        electionId=electionId
    )

    return result


def get_all(electionId=None, officeName=None, parentOfficeId=None, officeType=None):
    query = Model.query.join(
        Area.AreaAreaModel,
        Model.areaId == Area.AreaAreaModel.childAreaId,
        isouter=True
    )

    if officeName is not None:
        query = query.filter(Model.officeName.like(officeName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if officeType is not None:
        query = query.filter(Model.officeType == officeType)

    if parentOfficeId is not None:
        query = query.filter(Area.AreaAreaModel.parentAreaId == parentOfficeId)

    return query

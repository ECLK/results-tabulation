from app import db
from orm.entities import Office
from orm.enums import OfficeTypeEnum, AreaTypeEnum


class DistrictCentreModel(Office.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.DistrictCentre
    }


Model = DistrictCentreModel


def create(officeName, electionId):
    result = Model(
        officeName=officeName,
        electionId=electionId
    )

    return result

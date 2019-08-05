from app import db
from orm.entities import Office
from orm.enums import OfficeTypeEnum


class DistrictCentreModel(Office.Model):
    __mapper_args__ = {
        'polymorphic_identity': OfficeTypeEnum.DistrictCentre
    }


Model = DistrictCentreModel


def create(officeName, electionId, parentOfficeId=None):
    result = Model(
        officeName=officeName,
        electionId=electionId,
        parentOfficeId=parentOfficeId
    )
    db.session.add(result)
    db.session.commit()

    return result

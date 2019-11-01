from app import db
from orm.entities import Office
from orm.enums import OfficeTypeEnum, AreaTypeEnum
from sqlalchemy.orm import relationship, synonym


class CountingCentreModel(Office.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.CountingCentre
    }

    def __init__(self, officeName, electionId, registeredVotersCount=None):
        # For postal vote counting centres.
        if registeredVotersCount is not None:
            self._registeredVotersCount = registeredVotersCount

        super(CountingCentreModel, self).__init__(
            officeName=officeName,
            electionId=electionId
        )


Model = CountingCentreModel


def create(officeName, electionId, registeredVotersCount=None):
    result = Model(
        officeName=officeName,
        electionId=electionId,
        registeredVotersCount=registeredVotersCount
    )

    return result

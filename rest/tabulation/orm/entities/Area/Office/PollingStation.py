from orm.entities import Office
from orm.enums import AreaTypeEnum


class PollingStationModel(Office.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.PollingStation
    }

    def __init__(self, officeName, electionId, registeredVotersCount):
        self._registeredVotersCount = registeredVotersCount
        super(PollingStationModel, self).__init__(
            officeName=officeName,
            electionId=electionId
        )


Model = PollingStationModel


def create(officeName, electionId, registeredVotersCount):
    result = Model(
        officeName=officeName,
        electionId=electionId,
        registeredVotersCount=registeredVotersCount
    )

    return result


def get_all():
    query = Model.query

    return query

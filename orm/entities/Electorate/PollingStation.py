from config import db
from orm.entities import Electorate
from orm.entities.Electorate import PollingDistrict
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class PollingStationModel(Electorate.Model):
    pollingDivision = synonym("parentElectorate")
    electoralDistrict = association_proxy("parentElectorate", "electoralDistrict")
    country = association_proxy("electoralDistrict", "country")

    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.PollingStation
    }


Model = PollingStationModel


def get_by_id(pollingStationId):
    result = Model.query.filter(
        Model.electorateId == pollingStationId
    ).one_or_none()

    return result


def create(electionId, name, pollingDistrictId=None):
    country = PollingDistrict.get_by_id(pollingDistrictId=pollingDistrictId)

    if country is None:
        raise NotFoundException("Polling District not found (pollingDistrictId=%d)" % pollingDistrictId)
    else:
        polling_division = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=pollingDistrictId,
        )

        db.session.add(polling_division)
        db.session.add(polling_division)
        db.session.commit()

        return polling_division

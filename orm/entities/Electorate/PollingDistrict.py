from app import db
from orm.entities import Electorate
from orm.entities.Electorate import PollingDivision
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class PollingDistrictModel(Electorate.Model):
    pollingDivision = synonym("parentElectorate")
    electoralDistrict = association_proxy("parentElectorate", "electoralDistrict")
    country = association_proxy("electoralDistrict", "country")

    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.PollingDistrict
    }


Model = PollingDistrictModel


def get_by_id(pollingDistrictId):
    result = Model.query.filter(
        Model.electorateId == pollingDistrictId
    ).one_or_none()

    return result


def create(electionId, name, pollingDivisionId=None):
    country = PollingDivision.get_by_id(pollingDivisionId=pollingDivisionId)

    if country is None:
        raise NotFoundException("Polling Division not found (pollingDivisionId=%d)" % pollingDivisionId)
    else:
        polling_division = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=pollingDivisionId,
        )

        db.session.add(polling_division)
        db.session.add(polling_division)
        db.session.commit()

        return polling_division

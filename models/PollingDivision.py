from config import db
from orm.entities import Electorate
from orm.entities.Electorate import ElectoralDistrict
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class PollingDivisionModel(Electorate.Model):
    electoralDistrict = synonym("parentElectorate")
    country = association_proxy("parentElectorate", "country")

    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.PollingDivision
    }


Model = PollingDivisionModel


def get_by_id(pollingDivisionId):
    result = Model.query.filter(
        Model.electorateId == pollingDivisionId
    ).one_or_none()

    return result


def create(electionId, name, electoralDistrictId=None):
    country = ElectoralDistrict.get_by_id(electoralDistrictId=electoralDistrictId)

    if country is None:
        raise NotFoundException("Electoral District not found (electoralDistrictId=%d)" % electoralDistrictId)
    else:
        polling_division = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=electoralDistrictId,
        )

        db.session.add(polling_division)
        db.session.add(polling_division)
        db.session.commit()

        return polling_division

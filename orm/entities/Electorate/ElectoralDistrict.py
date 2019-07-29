from config import db
from orm.entities import Electorate
from orm.entities.Electorate import Country
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import synonym


class ElectoralDistrictModel(Electorate.Model):
    country = synonym("parentElectorate")

    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.ElectoralDistrict
    }


Model = ElectoralDistrictModel


def get_by_id(electoralDistrictId):
    result = Model.query.filter(
        Model.electorateId == electoralDistrictId
    ).one_or_none()

    return result


def create(electionId, name, countryId=None):
    country = Country.get_by_id(countryId=countryId)

    if country is None:
        raise NotFoundException("Country not found (countryId=%d)" % countryId)
    else:
        electoralDistrict = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=countryId,
        )

        db.session.add(electoralDistrict)
        db.session.add(electoralDistrict)
        db.session.commit()

        return electoralDistrict

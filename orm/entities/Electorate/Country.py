from app import db
from orm.entities import Electorate
from orm.enums import ElectorateTypeEnum, AreaTypeEnum
from sqlalchemy.ext.associationproxy import association_proxy


class CountryModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Country
    }


Model = CountryModel


def get_by_id(countryId):
    result = Model.query.filter(
        Model.electorateId == countryId
    ).one_or_none()

    return result


def create(electionId, name):
    country = Model(
        electorateName=name,
        electionId=electionId,
        parentElectorateId=None,
    )

    db.session.add(country)
    db.session.commit()

    return country

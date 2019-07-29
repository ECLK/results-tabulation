from config import db
from orm.entities import Electorate
from orm.enums import ElectorateTypeEnum

print("##### hey Electorate.Model ### ", Electorate)
print("##### hey Electorate.Model ### ", Electorate.Model)


class CountryModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.Country
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

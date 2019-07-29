from config import db
from orm.entities import Electorate
from orm.entities.Electorate import Country
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym


class ProvinceModel(Electorate.Model):
    # parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorateId"), nullable=True)

    country = synonym("parentElectorate")

    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.Province
    }


Model = ProvinceModel


def get_by_id(provinceId):
    result = Model.query.filter(
        Model.electorateId == provinceId
    ).one_or_none()

    return result


def create(electionId, name, countryId=None):
    country = Country.get_by_id(countryId=countryId)

    if country is None:
        raise NotFoundException("Country not found (countryId=%d)" % countryId)
    else:
        print("###### ")
        province = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=country.electorateId,
        )

        db.session.add(province)
        db.session.commit()

        return province

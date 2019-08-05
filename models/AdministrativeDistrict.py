from config import db
from orm.entities import Electorate
from orm.entities.Electorate import Province
from orm.enums import ElectorateTypeEnum
from exception import NotFoundException
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.associationproxy import association_proxy


class AdministrativeDistrictModel(Electorate.Model):
    __mapper_args__ = {
        'polymorphic_identity': ElectorateTypeEnum.AdministrativeDistrict
    }

    province = synonym("parentElectorate")
    country = association_proxy("parentElectorate", "country")


Model = AdministrativeDistrictModel


def get_by_id(administrativeDistrictId):
    result = Model.query.filter(
        Model.electorateId == administrativeDistrictId
    ).one_or_none()

    return result


def create(electionId, name, provinceId=None):
    province = Province.get_by_id(provinceId=provinceId)

    if province is None:
        raise NotFoundException("Province not found (provinceId=%d)" % provinceId)
    else:
        province = Model(
            electorateName=name,
            electionId=electionId,
            parentElectorateId=province.electorateId,
        )

        db.session.add(province)
        db.session.commit()

        return province

from config import db
from orm.entities import *
from orm.entities import *
from orm.entities.Electorate import Country, Province, AdministrativeDistrict
from orm.enums import ElectorateTypeEnum, StationaryItemTypeEnum, OfficeTypeEnum, FileTypeEnum

# db.engine.execute("create database election")


# Create the database
db.create_all()

# OFFICES = [
#     {"officeId": 0, "officeName": "Colombo", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 1, "officeName": "", "Moratuwa": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "Gampaha", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 2, "officeName": "Kalutara South", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 3, "officeName": "Kalutara North", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None}
# ]


election = Election.create()

country = Country.create(electionId=election.electionId, name="Sri Lanka")

province1 = Province.create(
    electionId=election.electionId,
    name="Colombo",
    countryId=country.electorateId
)

print(" ###### province1 ###### ", province1)
print(" ###### province1.parentElectorateId ###### ", province1.parentElectorateId)
print(" ###### province1.parentElectorate ###### ", province1.parentElectorate)
print(" ###### province1.country ###### ", province1.country)

administrativeDistrict1 = AdministrativeDistrict.create(
    electionId=election.electionId,
    name="Colombo",
    provinceId=province1.electorateId
)

administrativeDistrict2 = AdministrativeDistrict.create(
    electionId=election.electionId,
    name="Colombo",
    provinceId=province1.electorateId
)

print(" ###### administrativeDistrict1 ###### ", administrativeDistrict1)
print(" ###### administrativeDistrict1.parentElectorateId ###### ", administrativeDistrict1.parentElectorateId)
print(" ###### administrativeDistrict1.parentElectorate ###### ", administrativeDistrict1.parentElectorate)
print(" ###### administrativeDistrict1.province ###### ", administrativeDistrict1.province)
print(" ###### administrativeDistrict1.province.country ###### ", administrativeDistrict1.province.country)
print(" ###### administrativeDistrict1.country ###### ", administrativeDistrict1.country)
print(" ###### province1.childElectorates ###### ", province1.childElectorates)

# print(" ###### administrativeDistrict1 ###### ", administrativeDistrict1)
# print(" ###### administrativeDistrict1.province ###### ", administrativeDistrict1.province)
# print(" ###### administrativeDistrict1.country ###### ", administrativeDistrict1.country)

# for i in range(1, 2):
#     election = Election.create()
#     db.session.add(election)
#     db.session.commit()
#
#     for i in range(1, 6):
#         db.session.add(Party.create(
#             partyName="Party-%d" % i
#         ))
#         db.session.commit()
#
#     for j in range(1, 20):
#         db.session.add(Office.create(
#             electionId=election.electionId,
#             officeType=OfficeTypeEnum.DistrictCenter,
#             officeName="Office %d" % j
#         ))
#         db.session.add(Electorate.create(
#             electionId=election.electionId,
#             electorateType=ElectorateTypeEnum.AdministrativeDistrict,
#             electorateName="Electorate %d" % j
#         ))
#
#     for i in range(1, 10):
#         db.session.add(Ballot.create(
#             electionId=election.electionId,
#             ballotId="pre-ballot-%d-%d" % (election.electionId, i)
#         ))
#
#     for i in range(1, 50):
#         db.session.add(BallotBox.create(
#             electionId=election.electionId,
#             ballotBoxId="pre-ballot-box-%d-%d" % (election.electionId, i)
#         ))

db.session.commit()

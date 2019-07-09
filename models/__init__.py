from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

import enum


class ElectorateTypeEnum(enum.Enum):
    ElectionCommission = 1
    DistrictCenter = 2
    CountingCenter = 3


class OfficeTypeEnum(enum.Enum):
    Country = 1
    Province = 2
    AdministrativeDistrict = 3
    ElectoralDistrict = 4
    PollingDivision = 5
    PollingDistrict = 6
    PollingStation = 7


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class OfficeModel(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeType = db.Column(db.Enum(OfficeTypeEnum))
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    parentOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    election = relationship("ElectionModel", foreign_keys=[electionId])
    parentOffice = relationship("OfficeModel", foreign_keys=[parentOfficeId])

    electorates = relationship("ElectionModel", foreign_keys=[electionId])


class ElectorateModel(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateType = db.Column(db.Enum(ElectorateTypeEnum))
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorate.electorateId"))

    election = relationship("ElectionModel", foreign_keys=[electionId])
    parentElectorate = relationship("ElectorateModel", foreign_keys=[parentElectorateId])


class PartyModel(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    officeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"))

    election = relationship("ElectionModel", foreign_keys=[electionId])
    office = relationship("OfficeModel", foreign_keys=[officeId])
    latestVersion = relationship("TallySheetVersionModel", foreign_keys=[latestVersionId])


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheet_version'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"))

    createdBy = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tallySheet = relationship("TallySheetModel", foreign_keys=[tallySheetId])

    code = association_proxy('tallySheet', 'code')
    electionId = association_proxy('tallySheet', 'electionId')
    officeId = association_proxy('tallySheet', 'officeId')
    latestVersionId = association_proxy('tallySheet', 'latestVersionId')


class TallySheetPRE41Model(db.Model):
    __tablename__ = 'tallySheet_PRE-41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"),
                                    primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    countingCentreId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    party_wise_results = relationship("TallySheetPRE41PartyModel")

    tallySheetVersion = relationship("TallySheetVersionModel", foreign_keys=[tallySheetVersionId])
    electoralDistrict = relationship("OfficeModel", foreign_keys=[electoralDistrictId])
    pollingDivision = relationship("OfficeModel", foreign_keys=[pollingDivisionId])
    countingCentre = relationship("OfficeModel", foreign_keys=[countingCentreId])

    tallySheet = association_proxy('tallySheetVersion', 'tallySheet')
    code = association_proxy('tallySheetVersion', 'code')
    electionId = association_proxy('tallySheetVersion', 'electionId')
    officeId = association_proxy('tallySheetVersion', 'officeId')
    createdBy = association_proxy('tallySheetVersion', 'createdBy')
    createdAt = association_proxy('tallySheetVersion', 'createdAt')
    latestVersionId = association_proxy('tallySheetVersion', 'latestVersionId')


class TallySheetPRE41PartyModel(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_PRE-41.tallySheetVersionId"),
                                    primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey("party.partyId"), primary_key=True)
    voteCount = db.Column(db.Integer)

    party = relationship("PartyModel", foreign_keys=[partyId])
    tallySheetVersion = relationship("TallySheetPRE41Model", foreign_keys=[tallySheetVersionId])


class InvoiceModel(db.Model):
    __tablename__ = 'invoice'
    invoiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    issuingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    receivingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    election = relationship("ElectionModel", foreign_keys=[electionId])
    issuingOffice = relationship("OfficeModel", foreign_keys=[issuingOfficeId])
    receivingOffice = relationship("OfficeModel", foreign_keys=[receivingOfficeId])

    issuedBy = db.Column(db.Integer)
    issuedTo = db.Column(db.Integer)
    issuedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    stationaryItems = relationship("InvoiceStationaryItemModel")


class StationaryItemModel(db.Model):
    __tablename__ = 'stationaryItem'
    stationaryItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stationaryItemType = db.Column(db.String(10), index=True)


class InvoiceStationaryItemModel(db.Model):
    __tablename__ = 'invoice_stationaryItem'
    invoiceId = db.Column(db.Integer, db.ForeignKey("invoice.invoiceId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), primary_key=True)

    receivedBy = db.Column(db.Integer)
    receivedFrom = db.Column(db.Integer)
    receivedAt = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])

    stationaryItemType = association_proxy('stationaryItem', 'stationaryItemType')


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), primary_key=True)
    ballotId = db.Column(db.String(20), unique=True, nullable=False)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])


class BallotBoxModel(db.Model):
    __tablename__ = 'ballotBox'
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), primary_key=True)
    ballotBoxId = db.Column(db.String(20), unique=True, nullable=False)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])


# class TallySheet_PRE_34_CO(db.Model):
#     __tablename__ = 'tallySheet_PRE-34-CO'
#     tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
#     tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetI d"))
#     electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.id"))
#     pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.id"))
#     countingCentreId = db.Column(db.Integer, db.ForeignKey("office.id"))
#
#
# class TallySheet_PRE_34_CO__candidate(db.Model):
#     __tablename__ = 'tallySheet_PRE-34-CO__candidate'
#     tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
#     candidateId = db.Column(db.Integer, db.ForeignKey("candidate.id"), primary_key=True)
#     candidateId = db.Column(db.Integer, db.ForeignKey("candidate.id"), primary_key=True)
#     voteCount = db.Column(db.Integer)


ModelSchema = ma.ModelSchema

from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import enum


class ElectorateTypeEnum(enum.Enum):
    Country = 1
    Province = 2
    AdministrativeDistrict = 3
    ElectoralDistrict = 4
    PollingDivision = 5
    PollingDistrict = 6
    PollingStation = 7


class OfficeTypeEnum(enum.Enum):
    ElectionCommission = 1
    DistrictCenter = 2
    CountingCenter = 3


class StationaryItemTypeEnum(enum.Enum):
    Ballot = 1
    BallotBox = 2


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class OfficeModel(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeName = db.Column(db.String(100), nullable=False)
    officeType = db.Column(db.Enum(OfficeTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    parentOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    parentOffice = relationship("OfficeModel", foreign_keys=[parentOfficeId])
    electorates = relationship("ElectionModel", foreign_keys=[electionId])


class ElectorateModel(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateName = db.Column(db.String(100), nullable=False)
    electorateType = db.Column(db.Enum(ElectorateTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorate.electorateId"), nullable=True)

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
    code = db.Column(db.String(10), index=True, nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    office = relationship("OfficeModel", foreign_keys=[officeId])
    latestVersion = relationship("TallySheetVersionModel", foreign_keys=[latestVersionId])


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheet_version'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=False)

    createdBy = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

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
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    issuingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    receivingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    issuedBy = db.Column(db.Integer, nullable=False)
    issuedTo = db.Column(db.Integer, nullable=False)
    issuedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    delete = db.Column(db.Boolean, default=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    issuingOffice = relationship("OfficeModel", foreign_keys=[issuingOfficeId])
    receivingOffice = relationship("OfficeModel", foreign_keys=[receivingOfficeId])
    stationaryItems = relationship("InvoiceStationaryItemModel")


class StationaryItemModel(db.Model):
    __tablename__ = 'stationaryItem'
    stationaryItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stationaryItemType = db.Column(db.Enum(StationaryItemTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    invoiceStationaryItems = relationship("InvoiceStationaryItemModel")

    @hybrid_property
    def lockedInvoices(self):
        return [i for i in self.invoiceStationaryItems if i.delete == False]

    @hybrid_property
    def locked(self):
        return len([i for i in self.invoiceStationaryItems if i.delete == False]) > 0


class InvoiceStationaryItemModel(db.Model):
    __tablename__ = 'invoice_stationaryItem'
    invoiceId = db.Column(db.Integer, db.ForeignKey("invoice.invoiceId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), primary_key=True)
    received = db.Column(db.Boolean, default=False, nullable=False)
    receivedBy = db.Column(db.Integer, nullable=True)
    receivedFrom = db.Column(db.Integer, nullable=True)
    receivedAt = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, nullable=True)
    receivedOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=True)

    receivedOffice = relationship("OfficeModel", foreign_keys=[receivedOfficeId])
    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    invoice = relationship("InvoiceModel", foreign_keys=[invoiceId])

    delete = association_proxy('invoice', 'delete')


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    ballotId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), nullable=False,
                                 unique=True)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    election = relationship("ElectionModel", foreign_keys=[electionId])

    locked = association_proxy("stationaryItem", "locked")


class BallotBoxModel(db.Model):
    __tablename__ = 'ballotBox'
    ballotBoxId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), nullable=False,
                                 unique=True)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    election = relationship("ElectionModel", foreign_keys=[electionId])

    # locked = association_proxy("stationaryItem", "locked")


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

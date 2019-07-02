from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

import enum


class ElectorateType(enum.Enum):
    ElectionCommission = 1
    DistrictCenter = 2
    CountingCenter = 3


class OfficeType(enum.Enum):
    Country = 1
    Province = 2
    AdministrativeDistrict = 3
    ElectoralDistrict = 4
    PollingDivision = 5
    PollingDistrict = 6
    PollingStation = 7


class Election(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Office(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeType = db.Column(db.Enum(OfficeType))
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    parentOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    election = relationship("Election", foreign_keys=[electionId])

    electorates = relationship("Election", foreign_keys=[electionId])


class Electorate(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateType = db.Column(db.Enum(ElectorateType))
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorate.electorateId"))


class Ballot(db.Model):
    __tablename__ = 'ballot'
    ballotId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class BallotBox(db.Model):
    __tablename__ = 'ballotBox'
    ballotBoxId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class BallotBundle(db.Model):
    __tablename__ = 'ballotBundle'
    ballotBundleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ballotFromId = db.Column(db.Integer, db.ForeignKey("ballot.ballotId"))
    ballotToId = db.Column(db.Integer, db.ForeignKey("ballot.ballotId"))


class Party(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)


class TallySheet(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    officeId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"))

    election = relationship("Election", foreign_keys=[electionId], lazy='joined')
    office = relationship("Office", foreign_keys=[officeId], lazy='joined')
    latestVersion = relationship("TallySheetVersion", foreign_keys=[latestVersionId])


class TallySheetVersion(db.Model):
    __tablename__ = 'tallySheet_version'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"))

    createdBy = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tallySheet = relationship("TallySheet", foreign_keys=[tallySheetId])

    code = association_proxy('tallySheet', 'code')
    electionId = association_proxy('tallySheet', 'electionId')
    officeId = association_proxy('tallySheet', 'officeId')
    latestVersionId = association_proxy('tallySheet', 'latestVersionId')


class TallySheet_IssuingAndReceiving(db.Model):
    __tablename__ = 'tallySheet_issuingAndReceiving'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"),
                                    primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))

    ballotBundles = relationship("TallySheet_IssuingAndReceiving__BallotBundle")
    ballotBoxes = relationship("TallySheet_IssuingAndReceiving__BallotBox")


class TallySheet_IssuingAndReceiving__BallotBundle(db.Model):
    __tablename__ = 'tallySheet_issuingAndReceiving__ballotBundle'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_issuingAndReceiving.tallySheetVersionId"),
                                    primary_key=True)
    ballotBundleId = db.Column(db.Integer, db.ForeignKey("ballotBundle.ballotBundleId"), primary_key=True)

    ballotBundle = relationship("BallotBundle", foreign_keys=[ballotBundleId])

    ballotFromId = association_proxy('ballotBundle', 'ballotFromId')
    ballotToId = association_proxy('ballotBundle', 'ballotToId')


class TallySheet_IssuingAndReceiving__BallotBox(db.Model):
    __tablename__ = 'tallySheet_issuingAndReceiving__ballotBox'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_issuingAndReceiving.tallySheetVersionId"),
                                    primary_key=True)
    ballotBoxId = db.Column(db.Integer, db.ForeignKey("ballotBox.ballotBoxId"), primary_key=True)

    ballotBox = relationship("BallotBox", foreign_keys=[ballotBoxId])


class TallySheet_PRE_41(db.Model):
    __tablename__ = 'tallySheet_PRE-41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"),
                                    primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    countingCentreId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    party_wise_results = relationship("TallySheet_PRE_41__party")

    tallySheetVersion = relationship("TallySheetVersion", foreign_keys=[tallySheetVersionId])

    code = association_proxy('tallySheetVersion', 'code')
    electionId = association_proxy('tallySheetVersion', 'electionId')
    officeId = association_proxy('tallySheetVersion', 'officeId')
    createdBy = association_proxy('tallySheetVersion', 'createdBy')
    createdAt = association_proxy('tallySheetVersion', 'createdAt')
    latestVersionId = association_proxy('tallySheetVersion', 'latestVersionId')


class TallySheet_PRE_41__party(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_PRE-41.tallySheetVersionId"),
                                    primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey("party.partyId"), primary_key=True)
    voteCount = db.Column(db.Integer)


# class TallySheet_PRE_34_CO(db.Model):
#     __tablename__ = 'tallySheet_PRE-34-CO'
#     tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
#     tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
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

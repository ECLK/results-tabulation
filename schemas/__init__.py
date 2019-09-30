from marshmallow.fields import Integer, String

from app import db, ma
from orm.entities import StationaryItem, Ballot, Invoice, BallotBox, \
    Election, Proof, Submission, Electorate, SubmissionVersion, Area, Party, BallotBook
from orm.entities.Election import InvalidVoteCategory
from orm.entities.IO import File
from orm.entities.Invoice import InvoiceStationaryItem
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionCE201, TallySheetVersionPRE41, \
    TallySheetVersionPRE21, TallySheetVersion_PRE_30_PD, TallySheetVersion_PRE_30_ED
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201_PV, TallySheetVersionRow_CE_201, \
    TallySheetVersionRow_PRE_41, \
    TallySheetVersionRow_PRE_21, TallySheetVersionRow_PRE_ALL_ISLAND_RESULT, TallySheetVersionRow_PRE_30_ED, \
    TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_CE_201_PV_CC, TallySheetVersionRow_RejectedVoteCount
from orm.enums import StationaryItemTypeEnum, ProofTypeEnum, TallySheetCodeEnum, OfficeTypeEnum, \
    SubmissionTypeEnum, ElectorateTypeEnum, AreaTypeEnum, BallotTypeEnum, VoteTypeEnum

from marshmallow_enum import EnumField


class File_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "fileId",
            "fileName",
            "fileMimeType",
            "fileContentLength",
            "fileCreatedBy",
            "fileCreatedAt",
            "urlInline",
            "urlDownload"
        )

        model = File.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class CandidateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "candidateName",
            "candidateProfileImageFile"
        )

        model = Party.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    candidateProfileImageFile = ma.Nested(File_Schema)


class PartySchema(ma.ModelSchema):
    class Meta:
        fields = (
            "partyId",
            "partyName",
            "partySymbolFile",
            "partyAbbreviation",
            "candidates"
        )

        model = Party.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    partySymbolFile = ma.Nested(File_Schema)
    candidates = ma.Nested(CandidateSchema, many=True)


class ElectionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "electionId",
            "electionName",
            "parties",
            "invalidVoteCategories",
            "subElections",
            "voteType"
        )

        model = Election.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    voteType = EnumField(VoteTypeEnum)
    parties = ma.Nested(PartySchema, many=True)
    invalidVoteCategories = ma.Nested("InvalidVoteCategory_Schema", many=True)
    subElections = ma.Nested("self", only=["electionId", "electionName", "subElections", "voteType"], many=True)


class TallySheetVersionRow_PRE_41_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "count",
            "countInWords"
        )

        model = TallySheetVersionRow_PRE_41.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_PRE_41_Summary_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "rejectedVoteCount",
        )

        model = TallySheetVersionRow_RejectedVoteCount.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_PRE_ALL_ISLAND_RESULT_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "count"
        )

        model = TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_PRE_30_ED_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "pollingDivisionId",
            "count",
            "electionId",
            "voteType"
        )

        model = TallySheetVersionRow_PRE_30_ED.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    voteType = EnumField(VoteTypeEnum)


class TallySheetVersionRow_CE_201_PV_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetVersionRowId",
            "tallySheetVersionId",
            "ballotBoxStationaryItemId",
            "numberOfPacketsInserted",
            "numberOfAPacketsFound"
        )

        model = TallySheetVersionRow_CE_201_PV.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_CE_201_PV_CC_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetVersionRowId",
            "tallySheetVersionId",
            "countingCentreId",
            "situation",
            "timeOfCommencementOfCount",
            "numberOfAPacketsFound",
            "numberOfACoversRejected",
            "numberOfBCoversRejected",
            "numberOfValidBallotPapers"
        )

        model = TallySheetVersionRow_CE_201_PV_CC.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_PRE_30_PD_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "countingCentreId",
            "count"
        )

        model = TallySheetVersionRow_PRE_30_PD.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_AreaWiseSummary_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "rejectedVoteCount",
            "validVoteCount",
            "totalVoteCount",
        )

        model = TallySheetVersionRow_RejectedVoteCount.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_Summary_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaCount",
            "rejectedVoteCount",
            "validVoteCount",
            "totalVoteCount",
        )

        model = TallySheetVersionRow_RejectedVoteCount.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_PRE_21_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "count",
            "invalidVoteCategoryId",
            "categoryDescription"
        )

        model = TallySheetVersionRow_PRE_21.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionRow_CE_201_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "ballotBoxesIssued",
            "ballotBoxesReceived",
            "ballotsIssued",
            "ballotsReceived",
            "ballotsSpoilt",
            "ballotsUnused",
            "ordinaryBallotCountFromBoxCount",
            "tenderedBallotCountFromBoxCount",
            "ordinaryBallotCountFromBallotPaperAccount",
            "tenderedBallotCountFromBallotPaperAccount"
        )

        model = TallySheetVersionRow_CE_201.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # ballotBoxesIssued = ma.Nested("BallotBox_Schema", only=["ballotBoxId", "stationaryItemId"], many=True)
    # ballotBoxesReceived = ma.Nested("BallotBox_Schema", only=["ballotBoxId", "stationaryItemId"], many=True)


class AreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "areaType",
            "electionId",
            # "parents",
            # "children",
            # "pollingStations",
            # "countingCentres",
            # "districtCentres"
        )

        model = Area.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    areaType = EnumField(AreaTypeEnum)
    electorateType = EnumField(ElectorateTypeEnum)
    parents = ma.Nested('self', many=True)
    children = ma.Nested('self', only="areaId", many=True)
    pollingStations = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    countingCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    districtCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)


class ElectorateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "electorateId",
            "electorateName",
            "electorateType",
            "electionId",
            # "parents",
            # "children",
            # "pollingStations",
            # "countingCentres",
            # "districtCentres"
        )

        model = Electorate.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    electorateId = Integer()
    electorateName = String()
    electorateType = EnumField(ElectorateTypeEnum)
    parents = ma.Nested('AreaSchema', many=True)
    children = ma.Nested('AreaSchema', only="areaId", many=True)
    pollingStations = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    countingCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    districtCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)


class OfficeSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "officeId",
            "officeName",
            "officeType",
            "electionId",
            # "parents",
            # "children",
            # "pollingStations",
            # "countingCentres",
            # "districtCentres"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    electorateId = Integer()
    electorateName = String()
    officeType = EnumField(OfficeTypeEnum)
    parents = ma.Nested('AreaSchema', many=True)
    children = ma.Nested('AreaSchema', only="areaId", many=True)
    pollingStations = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    countingCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)
    districtCentres = ma.Nested('OfficeSchema', only=["officeId", "officeName", "officeType"], many=True)


class Proof_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "proofId",
            "proofType",
            "finished",
            "scannedFiles"
        )

        model = Proof.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    scannedFiles = ma.Nested(File_Schema, many=True)
    proofType = EnumField(ProofTypeEnum)


class SubmissionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "submissionId",
            "submissionType",
            "electionId",
            "area",
            "latestVersionId",
            # "tallySheetProofId",
            "submissionProofId",
            "versions"
        )

        model = Submission.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # latestVersion = ma.Nested(TallySheetVersionSchema)
    office = ma.Nested(OfficeSchema)
    electorate = ma.Nested(ElectorateSchema)
    submissionType = EnumField(SubmissionTypeEnum)
    submissionProof = ma.Nested(Proof_Schema)


class SubmissionVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "submissionVersionId",
            # "submission",
            "createdBy",
            "createdAt"
        )

        model = SubmissionVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "contentUrl"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)


class TallySheetVersionPRE41Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content",
            "summary"
        )

        model = TallySheetVersionPRE41.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_PRE_41_Schema, many=True)
    summary = ma.Nested(TallySheetVersionRow_PRE_41_Summary_Schema)


class TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content"
        )

        model = TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_PRE_ALL_ISLAND_RESULT_Schema, many=True)


class TallySheetVersion_CE_201_PV_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content",
            "summary"
        )

        model = TallySheetVersionRow_CE_201_PV.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_CE_201_PV_Schema, many=True)
    summary = ma.Nested(TallySheetVersionRow_CE_201_PV_CC_Schema)


class TallySheetVersion_PRE_30_ED_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content",
            "areaWiseSummary",
            "summary"
        )

        model = TallySheetVersion_PRE_30_ED.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_PRE_30_ED_Schema, many=True)
    areaWiseSummary = ma.Nested(TallySheetVersionRow_AreaWiseSummary_Schema, many=True)
    summary = ma.Nested(TallySheetVersionRow_Summary_Schema, many=False)


class TallySheetVersion_PRE_30_PD_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content",
            "areaWiseSummary",
            "summary"
        )

        model = TallySheetVersion_PRE_30_PD.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_PRE_30_PD_Schema, many=True)
    areaWiseSummary = ma.Nested(TallySheetVersionRow_AreaWiseSummary_Schema, many=True)
    summary = ma.Nested(TallySheetVersionRow_Summary_Schema, many=False)


class TallySheetVersionPRE21Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content"
        )

        model = TallySheetVersionPRE21.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_PRE_21_Schema, many=True)


class TallySheetVersionCE201Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "htmlUrl",
            "content"
        )

        model = TallySheetVersionCE201.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_CE_201_Schema, many=True)


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            "electionId",
            "office",
            "latestVersionId",
            # "latestVersion",
            "submissionProofId",
            "versions"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    tallySheetCode = EnumField(TallySheetCodeEnum)
    office = ma.Nested(AreaSchema)
    versions = ma.Nested(SubmissionVersionSchema, only="submissionVersionId", many=True)
    latestVersion = ma.Nested(SubmissionVersionSchema)
    submissionProof = ma.Nested(Proof_Schema)


# class TallySheet_PRE_41__party_Schema(ma.ModelSchema):
#     class Meta:
#         fields = ("partyId", "voteCount")
#
#         model = TallySheetPRE41Party.Model
#         # optionally attach a Session
#         # to use for deserialization
#         sqla_session = db.session


# class TallySheet_PRE_41_Schema(ma.ModelSchema):
#     class Meta:
#         fields = (
#             "tallySheetId",
#             "tallySheetCode",
#             "electionId",
#             "officeId",
#             "latestVersionId",
#
#             "tallySheetVersionId",
#             "createdBy",
#             "createdAt",
#
#             "electoralDistrictId",
#             "countingCentreId",
#             "countingCentreId",
#             "party_wise_results",
#         )
#
#         model = TallySheetPRE41.Model
#         # optionally attach a Session
#         # to use for deserialization
#         sqla_session = db.session
#
#     createdBy = ma.Integer()
#     createdAt = ma.String()
#
#     party_wise_results = ma.Nested(TallySheet_PRE_41__party_Schema, many=True)


class StationaryItem_Schema(ma.ModelSchema):
    stationaryItemType = EnumField(StationaryItemTypeEnum)

    class Meta:
        fields = (
            "stationaryItemId",
            "stationaryItemType",
            "electionId",
            "available"
        )

        model = StationaryItem.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Invoice_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invoiceId",
            "electionId",
            "issuingOfficeId",
            "receivingOfficeId",
            "issuedBy",
            "issuedTo",
            "issuedAt",
            "confirmed",
            "delete"
        )

        model = Invoice.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Invoice_StationaryItem_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "received",
            "receivedBy",
            "receivedFrom",
            "receivedOfficeId",
            "receivedAt",
            # "receivedProofId",
            "invoiceId",
            "stationaryItemId",
            "stationaryItem",
            "delete",
            "receivedProof"
        )

        model = InvoiceStationaryItem.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    invoice = ma.Nested(Invoice_Schema)
    stationaryItem = ma.Nested(StationaryItem_Schema)
    receivedProof = ma.Nested(Proof_Schema)


class InvalidVoteCategory_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invalidVoteCategoryId",
            "categoryDescription"
        )

        model = InvalidVoteCategory.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Ballot_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotId",
            "ballotType",
            "electionId",
            "stationaryItemId",
            "available"
        )

        model = Ballot.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    ballotType = EnumField(BallotTypeEnum)
    stationaryItem = ma.Nested(StationaryItem_Schema)


class BallotBox_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotBoxId",
            "electionId",
            "stationaryItemId",
            "available"
        )

        model = BallotBox.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)


class BallotBookSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "stationaryItemId",
            "electionId",
            "fromBallotId",
            "toBallotId",
            "ballots",
            "available"
        )

        model = BallotBook.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)
    ballots = ma.Nested(Ballot_Schema, only=["ballotId", "stationaryItemId", "ballotType"], many=True)

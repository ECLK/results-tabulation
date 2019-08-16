from marshmallow.fields import Integer, String

from app import db, ma
from orm.entities import StationaryItem, Ballot, Invoice, BallotBox, \
    Election, Proof, Submission, Electorate, SubmissionVersion, Area, Party
from orm.entities.IO import File
from orm.entities.Invoice import InvoiceStationaryItem
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.Submission import TallySheet
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.enums import StationaryItemTypeEnum, ProofTypeEnum, TallySheetCodeEnum, OfficeTypeEnum, ReportCodeEnum, \
    SubmissionTypeEnum, ElectorateTypeEnum, AreaTypeEnum

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
            "parties"
        )

        model = Election.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    parties = ma.Nested(PartySchema, many=True)


class PartyCountSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "partyId",
            "count",
            "countInWords"
        )

        model = PartyCount.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            # "electionId",
            # "officeId",
            # "latestVersionId",

            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "tallySheetContent"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    tallySheetCode = EnumField(TallySheetCodeEnum)
    tallySheetContent = ma.Nested(PartyCountSchema, many=True)


class AreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "areaType",
            "electionId",
            "parents",
            "children",
            "pollingStations",
            "countingCentres",
            "districtCentres"
        )

        model = Area.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    areaType = EnumField(AreaTypeEnum)
    electorateType = EnumField(ElectorateTypeEnum)
    parents = ma.Nested('self', many=True)
    children = ma.Nested('self', only="areaId", many=True)
    pollingStations = ma.Nested('self', only="areaId", many=True)
    countingCentres = ma.Nested('self', only="areaId", many=True)
    districtCentres = ma.Nested('self', only="areaId", many=True)


class ElectorateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "electorateId",
            "electorateName",
            "electorateType",
            "electionId",
            # "parents",
            # "children",
            "pollingStations",
            "countingCentres",
            "districtCentres"
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
    pollingStations = ma.Nested('AreaSchema', many=True)
    countingCentres = ma.Nested('AreaSchema', many=True)
    districtCentres = ma.Nested('AreaSchema', many=True)


class OfficeSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "officeId",
            "officeName",
            "officeType",
            "electionId",
            # "parents",
            # "children",
            "pollingStations",
            "countingCentres",
            "districtCentres"
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
    pollingStations = ma.Nested('AreaSchema', many=True)
    countingCentres = ma.Nested('AreaSchema', many=True)
    districtCentres = ma.Nested('AreaSchema', many=True)


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
            "parents",
            "children",
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
            "submissionVersionId",
            "submission",
            "createdBy",
            "createdAt"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)


class ReportVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "reportId",
            "reportVersionId",
            "createdBy",
            "createdAt",
            "reportFile"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    reportFile = ma.Nested(File_Schema)


class TallySheetVersionPRE41Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            "tallySheetContent"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    # submission = ma.Nested(SubmissionSchema)
    tallySheetContent = ma.Nested(PartyCountSchema, many=True)


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            "electionId",
            "office",
            "latestVersionId",
            "latestVersion",
            "parents",
            "children",
            "submissionProofId",
            "versions"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    tallySheetCode = EnumField(TallySheetCodeEnum)
    office = ma.Nested(OfficeSchema)
    versions = ma.Nested(SubmissionVersionSchema, only="submissionVersionId", many=True)
    latestVersion = ma.Nested(SubmissionVersionSchema)
    parents = ma.Nested(SubmissionSchema, only="submissionId", many=True)
    children = ma.Nested(SubmissionSchema, many=True)
    submissionProof = ma.Nested(Proof_Schema)


class ReportSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "reportId",
            "reportCode",
            "electionId",
            "area",
            "areaId",
            "latestVersionId",
            "parents",
            "children",
            "submissionProofId",
            "submission",
            "versions"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    reportCode = EnumField(ReportCodeEnum)
    area = ma.Nested(AreaSchema)
    versions = ma.Nested(SubmissionVersionSchema, only="submissionVersionId", many=True)
    parents = ma.Nested(SubmissionSchema, only="submissionId", many=True)
    children = ma.Nested(SubmissionSchema, many=True)
    submission = ma.Nested(SubmissionSchema)
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
#             "pollingDivisionId",
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
            "locked"
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


class Ballot_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotId",
            "electionId",
            "stationaryItemId",
            "stationaryItem"
        )

        model = Ballot.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)


class BallotBox_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotBoxId",
            "electionId",
            "stationaryItemId",
            "stationaryItem"
        )

        model = BallotBox.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    stationaryItem = ma.Nested(StationaryItem_Schema)

from marshmallow.fields import Integer, String

from app import db, ma
from orm.entities import StationaryItem, Ballot, Invoice, BallotBox, \
    Election, Proof, Submission, Electorate, SubmissionVersion, Area, Party, BallotBook, Candidate, Template, \
    TallySheetVersionRow
from orm.entities.Area import AreaAreaModel
from orm.entities.Audit import Stamp
from orm.entities.Election import InvalidVoteCategory, ElectionCandidate
from orm.entities.IO import File
from orm.entities.Invoice import InvoiceStationaryItem
from orm.entities.Meta import MetaData
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel
from orm.enums import StationaryItemTypeEnum, ProofTypeEnum, OfficeTypeEnum, SubmissionTypeEnum, ElectorateTypeEnum, \
    AreaTypeEnum, BallotTypeEnum
from marshmallow_enum import EnumField


class StampSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "stampId",
            "createdBy",
            "createdAt"
        )

        model = Stamp.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class MetaDataSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "metaDataKey",
            "metaDataValue"
        )

        model = MetaData.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


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
            "candidateProfileImageFile",
            "qualifiedForPreferences"
        )

        model = ElectionCandidate.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    candidateProfileImageFile = ma.Nested(File_Schema)


class PartySchema(ma.ModelSchema):
    class Meta:
        fields = (
            "partyId",
            "partyName",
            "partySymbol",
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
            "electionTemplateName",
            "parties",
            "invalidVoteCategories",
            "subElections",
            "voteType",
            "rootElectionId",
            "rootElection",
            "parentElection"
        )

        model = Election.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    parties = ma.Nested(PartySchema, many=True)
    invalidVoteCategories = ma.Nested("InvalidVoteCategory_Schema", many=True)
    subElections = ma.Nested("self", only=["electionId", "electionName", "subElections", "voteType", "rootElectionId",
                                           "rootElection", "parties"], many=True)
    rootElection = ma.Nested("self", only=[
        "electionId", "electionName", "voteType", "electionTemplateName", "parties", "invalidVoteCategories"
    ])
    parentElection = ma.Nested("self", only=[
        "electionId", "electionName", "voteType", "electionTemplateName", "parties", "invalidVoteCategories"
    ])


class TallySheetVersionRow_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetVersionRowId",
            "templateRowId",
            "templateRowType",
            "areaId",
            "areaName",
            "candidateId",
            "candidateName",
            "partyId",
            "partyName",
            "numValue",
            "strValue"
        )

        model = TallySheetVersionRow.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class SimpleAreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "areaType",
            "electionId",
            "parents",
            "children"
        )

        model = Area.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    areaType = EnumField(AreaTypeEnum)
    electorateType = EnumField(ElectorateTypeEnum)
    # parents = ma.Nested('self', only="areaId", many=True)
    children = ma.Nested('AreaAreaSchema', only="childAreaId", many=True)
    parents = ma.Nested('AreaAreaSchema', only="parentAreaId", many=True)


class AreaAreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "parentAreaId",
            "childAreaId"
        )

        model = AreaAreaModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class AreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "areaType",
            "electionId",
            # "parents",
            "children",
            # "pollingStations",
            # "countingCentres",
            # "districtCentres",
            # "pollingDistricts",
            # "electoralDistricts",
            # "pollingDivisions"
        )

        model = Area.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    areaType = EnumField(AreaTypeEnum)
    electorateType = EnumField(ElectorateTypeEnum)
    parents = ma.Nested('self', many=True)
    children = ma.Nested('self', only="areaId", many=True)
    pollingStations = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    countingCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    districtCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    pollingDistricts = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    electoralDistricts = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    pollingDivisions = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)


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
    pollingStations = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    countingCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    districtCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)


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
    pollingStations = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    countingCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)
    districtCentres = ma.Nested('AreaSchema', only=["areaId", "areaName", "areaType"], many=True)


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
            "areaId",
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
            # "htmlUrl",
            # "contentUrl",
            "content",
            "isComplete"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    submission = EnumField(SubmissionSchema)
    content = ma.Nested(TallySheetVersionRow_Schema, many=True)


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            "templateId",
            "template",
            "electionId",
            "areaId",
            "latestVersionId",
            "latestStamp",
            "lockedVersionId",
            "lockedStamp",
            "submittedVersionId",
            "submittedStamp",
            "locked",
            "submitted",
            "notified",
            "released",
            # "latestVersion",
            "submissionProofId",
            "versions",
            "metaDataList"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    template = ma.Nested("TemplateSchema")
    area = ma.Nested(AreaSchema)
    versions = ma.Nested(SubmissionVersionSchema, only="submissionVersionId", many=True)
    latestVersion = ma.Nested(SubmissionVersionSchema)
    latestStamp = ma.Nested(StampSchema)
    lockedStamp = ma.Nested(StampSchema)
    submittedStamp = ma.Nested(StampSchema)
    submissionProof = ma.Nested(Proof_Schema)
    metaDataList = ma.Nested(MetaDataSchema, many=True)


class TemplateRowSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "templateRowId",
            "templateRowType",
            "hasMany",
            "isDerived"
        )

        model = TemplateRowModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TemplateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "templateId",
            "templateName",
            "rows",
            "isDerived"
        )

        model = Template.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    rows = ma.Nested(TemplateRowSchema, many=True)


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

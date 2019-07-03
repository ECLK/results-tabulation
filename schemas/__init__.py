from config import db, ma
from models import ElectionModel, TallySheetModel, TallySheetVersionModel, TallySheetPRE41Model, TallySheetPRE41PartyModel, InvoiceModel, \
    InvoiceItemModel, InvoiceInvoiceItemModel, BallotBoxModel, BallotModel

from marshmallow import Schema, fields, validates_schema, ValidationError


class ElectionSchema(ma.ModelSchema):
    class Meta:
        model = ElectionModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "code",
            "electionId",
            "officeId",
            "latestVersionId",

            "tallySheetVersionId",
            "createdBy",
            "createdAt"
        )

        model = TallySheetVersionModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        model = TallySheetModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    latestVersion = ma.Nested(TallySheetVersionSchema)


class TallySheet_PRE_41__party_Schema(ma.ModelSchema):
    class Meta:
        fields = ("partyId", "voteCount")

        model = TallySheetPRE41PartyModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheet_PRE_41_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "code",
            "electionId",
            "officeId",
            "latestVersionId",

            "tallySheetVersionId",
            "createdBy",
            "createdAt",

            "electoralDistrictId",
            "pollingDivisionId",
            "countingCentreId",
            "party_wise_results",
        )

        model = TallySheetPRE41Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    createdBy = ma.Integer()
    createdAt = ma.String()

    party_wise_results = ma.Nested(TallySheet_PRE_41__party_Schema, many=True)


class InvoiceItem_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invoiceId",
            "invoiceItemType"
        )

        model = InvoiceModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Invoice_InvoiceItem_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invoiceId",
            "invoiceItemId",
            "receivedBy",
            "receivedFrom",
            "receivedAt"
        )

        model = InvoiceInvoiceItemModel
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
            "invoiceItems"
        )

        model = InvoiceModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    invoiceItems = ma.Nested(Invoice_InvoiceItem_Schema, many=True)


class Ballot_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotId",
            "invoiceItemId"
        )

        model = BallotModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class BallotBox_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "ballotBoxId",
            "invoiceItemId"
        )

        model = BallotBoxModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

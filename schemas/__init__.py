from config import db, ma
from models import Election, TallySheet, TallySheetVersion, TallySheet_PRE_41, TallySheet_PRE_41__party

from marshmallow import Schema, fields, validates_schema, ValidationError


class ElectionSchema(ma.ModelSchema):
    class Meta:
        model = Election
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        model = TallySheetVersion
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheetSchema(ma.ModelSchema):
    class Meta:
        model = TallySheet
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    latestVersion = ma.Nested(TallySheetVersionSchema)


class TallySheet_PRE_41__party_Schema(ma.ModelSchema):
    class Meta:
        fields = ("partyId", "voteCount")

        model = TallySheet_PRE_41__party
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TallySheet_PRE_41_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetVersionId",
            "tallySheetId",
            "electoralDistrictId",
            "pollingDivisionId",
            "countingCentreId",
            "party_wise_results",
            "createdBy",
            "createdAt",
            "electionId",
            "officeId",
            "code",
            "latestVersionId"
        )

        model = TallySheet_PRE_41
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    createdBy = ma.Integer()
    createdAt = ma.String()

    party_wise_results = ma.Nested(TallySheet_PRE_41__party_Schema, many=True)

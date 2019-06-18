from config import db, ma
from models import Election, TallySheet, TallySheetVersion


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

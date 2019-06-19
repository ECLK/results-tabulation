"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import jsonify
from flask import make_response, abort
from config import db
from models import TallySheet, TallySheetVersion, TallySheet_PRE_41
from schemas import TallySheetSchema, TallySheetVersionSchema, TallySheet_PRE_41_Schema, TallySheet_PRE_41__party_Schema


def getAll():
    """
        return all tally sheets
    """

    # Create the list of tally sheets from our data
    people = TallySheetVersion.query.all()

    # Serialize the data for the response
    person_schema = TallySheetVersionSchema(many=True)
    data = person_schema.dump(people).data
    return data


def get_by_id(tallySheetId):
    print("################tallySheetId####", tallySheetId)

    # person = Person.query.filter(Person.person_id == person_id).one_or_none()

    tallySheet = TallySheet.query.filter(TallySheet.tallySheetId == tallySheetId).one_or_none()

    print("##### tallySheet.latestVersionId ###", tallySheet.latestVersionId)

    # tallySheet_PRE_41 = TallySheetVersion.query. \
    #     join(TallySheet, TallySheet.id == TallySheetVersion.tallySheetId). \
    #     join(TallySheet_PRE_41, TallySheet_PRE_41.tallySheetVersionId == TallySheetVersion.id). \
    #     add_columns(
    #     TallySheet.id.label("tallySheetId"),
    #     TallySheet.code.label("code"),
    #     TallySheetVersion.id.label("tallySheetVersionId"),
    #     TallySheetVersion.createdBy.label("createdBy"),
    #     TallySheetVersion.createdAt.label("createdAt"),
    #     TallySheet_PRE_41.countingCentreId.label("countingCentreId"),
    #     TallySheet_PRE_41.electoralDistrictId.label("electoralDistrictId"),
    #     TallySheet_PRE_41.pollingDivisionId.label("pollingDivisionId")
    # ) \
    #     .filter(TallySheetVersion.id == tallySheet.latestVersionId).one_or_none()

    # tallySheet_PRE_41 = TallySheet_PRE_41.query. \
    #     join(TallySheetVersion, TallySheet_PRE_41.tallySheetVersionId == TallySheetVersion.id). \
    #     join(TallySheet, TallySheet.id == TallySheetVersion.tallySheetId). \
    #     add_columns(
    #     TallySheet.id.label("tallySheetId"),
    #     TallySheet.code.label("code"),
    #     TallySheetVersion.id.label("tallySheetVersionId"),
    #     TallySheetVersion.createdBy.label("createdBy"),
    #     TallySheetVersion.createdAt.label("createdAt"),
    #     TallySheet_PRE_41.countingCentreId.label("countingCentreId"),
    #     TallySheet_PRE_41.electoralDistrictId.label("electoralDistrictId"),
    #     TallySheet_PRE_41.pollingDivisionId.label("pollingDivisionId"),
    #     TallySheet_PRE_41.party_wise_results.label("party_wise_results")
    # ) \
    #     .filter(TallySheetVersion.id == tallySheet.latestVersionId).one_or_none()

    tallySheet_PRE_41 = TallySheet_PRE_41.query.filter(
        TallySheet_PRE_41.tallySheetVersionId == tallySheet.latestVersionId).one_or_none()

    # print("#####", tallySheet_PRE_41.__dict__)

    person_schema = TallySheet_PRE_41_Schema()
    data = person_schema.dump(tallySheet_PRE_41).data
    return data


def create_tallysheet_PRE_41__party(body, tallysheetVersion):
    schema = TallySheet_PRE_41__party_Schema()

    for party_wise_entry_body in body["table"]:
        new_tallysheet_PRE_41__party = schema.load(party_wise_entry_body, session=db.session).data
        new_tallysheet_PRE_41__party.tallySheetVersionId = tallysheetVersion.tallySheetVersionId
        new_tallysheet_PRE_41__party.partyId = party_wise_entry_body["partyId"]

        db.session.add(new_tallysheet_PRE_41__party)
        db.session.commit()


def create_tallysheet_PRE_41(body, tallysheetVersion):
    schema = TallySheet_PRE_41_Schema()
    new_tallysheet_PRE_41 = schema.load(body, session=db.session).data
    new_tallysheet_PRE_41.tallySheetId = tallysheetVersion.tallySheetId
    new_tallysheet_PRE_41.tallySheetVersionId = tallysheetVersion.tallySheetVersionId

    db.session.add(new_tallysheet_PRE_41)
    db.session.commit()

    create_tallysheet_PRE_41__party(body, tallysheetVersion)


def create_tallysheet_version(body, tallysheet):
    """
        Create new tally sheet version and append it as the latest version.
    """

    # to avoid merging when there's an id passed through the request.
    body.pop('id', None)

    # Create an instance using the schema and the passed-in data
    schema = TallySheetVersionSchema()
    new_tallysheet_version = schema.load(body, session=db.session).data
    new_tallysheet_version.tallySheetId = tallysheet.tallySheetId

    db.session.add(new_tallysheet_version)
    db.session.commit()

    tallysheet.latestVersion = new_tallysheet_version
    db.session.commit()

    create_tallysheet_PRE_41(body, new_tallysheet_version)

    return new_tallysheet_version


def create(body):
    """
        Create new tally sheet.
    """

    # to avoid merging when there's an id passed through the request.
    body.pop('id', None)

    # Create an instance using the schema and the passed-in data
    schema = TallySheetSchema()
    new_tallysheet = schema.load(body, session=db.session).data

    # Add the entry to the database
    db.session.add(new_tallysheet)
    db.session.commit()

    create_tallysheet_version(body, new_tallysheet)

    # Serialize and return the newly created entry in the response
    return schema.dump(new_tallysheet).data, 201


def update(tallySheetId, body):
    """
        Append new version to the tally sheet.
    """
    # Get the tally sheet
    tallySheet = TallySheet.query.filter(
        TallySheet.tallySheetId == tallySheetId
    ).one_or_none()

    if tallySheet is None:
        abort(
            404,
            "Tally Sheet not found for Id: {tallySheetId}".format(tallySheetId=tallySheetId),
        )

    create_tallysheet_version(body, tallySheet)

    schema = TallySheetVersionSchema()

    return schema.dump(new_tallysheet).data, 201

"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import TallySheet, TallySheetVersion, TallySheet_PRE_41, TallySheet_PRE_41__party
from schemas import TallySheetSchema, TallySheetVersionSchema, TallySheet_PRE_41_Schema


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
    tallySheet = TallySheet.query.filter(TallySheet.tallySheetId == tallySheetId).one_or_none()

    tallySheet_PRE_41 = TallySheet_PRE_41.query.filter(
        TallySheet_PRE_41.tallySheetVersionId == tallySheet.latestVersionId).one_or_none()

    person_schema = TallySheet_PRE_41_Schema()
    data = person_schema.dump(tallySheet_PRE_41).data
    return data


def create_tallysheet_PRE_41__party(body, tallysheetVersion):
    for party_wise_entry_body in body["table"]:
        new_tallysheet_PRE_41__party = TallySheet_PRE_41__party(
            partyId=party_wise_entry_body["partyId"],
            tallySheetVersionId=tallysheetVersion.tallySheetVersionId
        )

        db.session.add(new_tallysheet_PRE_41__party)
        db.session.commit()


def create_tallysheet_PRE_41(body, tallysheetVersion):
    new_tallysheet_PRE_41 = TallySheet_PRE_41(
        tallySheetId=tallysheetVersion.tallySheetId,
        tallySheetVersionId=tallysheetVersion.tallySheetVersionId,
        electoralDistrictId=body["electoralDistrictId"],
        pollingDivisionId=body["pollingDivisionId"],
        countingCentreId=body["countingCentreId"],
    )

    db.session.add(new_tallysheet_PRE_41)
    db.session.commit()

    create_tallysheet_PRE_41__party(body, tallysheetVersion)


def create_tallysheet_version(body, tallysheet):
    """
        Create new tally sheet version and append it as the latest version.
    """
    new_tallysheet_version = TallySheetVersion(
        tallySheetId=tallysheet.tallySheetId,
        createdBy=12  # TODO
    )

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

    new_tallysheet = TallySheet(
        electionId=body["electionId"],
        officeId=body["officeId"]
    )

    # Add the entry to the database
    db.session.add(new_tallysheet)
    db.session.commit()

    create_tallysheet_version(body, new_tallysheet)

    # Serialize and return the newly created entry in the response
    return TallySheetSchema().dump(new_tallysheet).data, 201


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

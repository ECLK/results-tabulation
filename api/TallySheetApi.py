from flask import abort
from app import db
from orm.entities.TallySheet import Model as TallySheetModel
from orm.entities.History import Model as TallySheetVersionModel
from schemas import TallySheetSchema
from api import tallySheetPRE41Api
from util import RequestBody, Auth

from schemas import TallySheetSchema as Schema
from orm.entities import TallySheet


def getAll(electionId=None, officeId=None):
    result = TallySheet.get_all(
        electionId=electionId,
        officeId=officeId
    )

    return Schema(many=True).dump(result).data


def get_by_id(tallySheetId):
    tallySheet = TallySheetModel.query.filter(TallySheetModel.tallySheetId == tallySheetId).one_or_none()

    return TallySheetSchema().dump(tallySheet).data


def create_tallysheet_version(body, tallysheet):
    new_tallysheet_version = TallySheetVersionModel(
        tallySheetId=tallysheet.tallySheetId,
        createdBy=Auth().get_user_id()
    )

    db.session.add(new_tallysheet_version)
    db.session.commit()

    tallysheet.latestVersion = new_tallysheet_version
    db.session.commit()

    if tallysheet.code == "PRE-41":
        return tallySheetPRE41Api.create(body, new_tallysheet_version)
    else:
        return new_tallysheet_version


def create(body):
    request_body = RequestBody(body)
    new_tallysheet = TallySheetModel(
        electionId=request_body.get("electionId"),
        code=request_body.get("code"),
        officeId=request_body.get("officeId")
    )

    # Add the entry to the database
    db.session.add(new_tallysheet)
    db.session.commit()

    new_tallysheet = create_tallysheet_version(body, new_tallysheet)

    # Serialize and return the newly created entry in the response
    return get_tallysheet_response(new_tallysheet), 201


def get_tallysheet_response(new_tallysheet):
    if new_tallysheet.code == "PRE-41":
        return TallySheetSchema().dump(new_tallysheet).data
    else:
        return TallySheetSchema().dump(new_tallysheet).data


def update(tallySheetId, body):
    # Get the tally sheet
    tallySheet = TallySheetModel.query.filter(
        TallySheetModel.tallySheetId == tallySheetId
    ).one_or_none()

    if tallySheet is None:
        abort(
            404,
            "Tally Sheet not found for Id: {tallySheetId}".format(tallySheetId=tallySheetId),
        )

    create_tallysheet_version(body, tallySheet)

    schema = TallySheetSchema()

    return schema.dump(new_tallysheet).data, 201

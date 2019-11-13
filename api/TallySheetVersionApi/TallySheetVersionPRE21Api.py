from app import db
from auth import authorize, POLLING_DIVISION_REPORT_VERIFIER_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from util import RequestBody
from schemas import TallySheetVersionPRE21Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet


@authorize(required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE21Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_21
    )
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        is_complete = True
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            count = party_count_body.get("count")
            invalidVoteCategoryId = party_count_body.get("invalidVoteCategoryId")

            if (count and invalidVoteCategoryId) is not None:
                tallySheetVersion.add_row(
                    count=count,
                    invalidVoteCategoryId=invalidVoteCategoryId
                )
            else:
                is_complete = False

        if is_complete:
            tallySheetVersion.set_complete()
    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data

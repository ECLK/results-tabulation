from app import db
from auth import authorize, EC_LEADERSHIP_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE
from exception import NotFoundException
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetVersionPRE41Schema, TallySheetVersionSchema
from util import RequestBody


@authorize(required_roles=[DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE41Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_41
    )
    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_30_PD
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            tallySheetVersion.add_row(
                candidateId=party_count_body.get("candidateId"),
                count=party_count_body.get("count"),
                countInWords=party_count_body.get("countInWords")
            )

    tally_sheet_summary_body = request_body.get("summary")
    if tally_sheet_summary_body is not None:
        tallySheetVersion.add_invalid_vote_count(
            electionId=tallySheetVersion.submission.electionId,
            rejectedVoteCount=tally_sheet_summary_body.get("rejectedVoteCount")
        )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data

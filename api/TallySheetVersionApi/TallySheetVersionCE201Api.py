from api import TallySheetVersionApi
from app import db
from auth import authorize
from auth.AuthConstants import DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from util import RequestBody
from schemas import TallySheetVersionCE201Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet


@authorize(required_roles=[DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionCE201Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.CE_201
    )

    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for party_count_body in tally_sheet_content:
            party_count_body = RequestBody(party_count_body)
            tallySheetVersionRow = tallySheetVersion.add_row(
                areaId=party_count_body.get("areaId"),
                ballotsIssued=party_count_body.get("ballotsIssued"),
                ballotsReceived=party_count_body.get("ballotsReceived"),
                ballotsSpoilt=party_count_body.get("ballotsSpoilt"),
                ballotsUnused=party_count_body.get("ballotsUnused"),
                ordinaryBallotCountFromBoxCount=party_count_body.get("ordinaryBallotCountFromBoxCount"),
                tenderedBallotCountFromBoxCount=party_count_body.get("tenderedBallotCountFromBoxCount"),
                ordinaryBallotCountFromBallotPaperAccount=party_count_body.get(
                    "ordinaryBallotCountFromBallotPaperAccount"),
                tenderedBallotCountFromBallotPaperAccount=party_count_body.get(
                    "tenderedBallotCountFromBallotPaperAccount")
            )

            for issued_ballot_box_id in party_count_body.get("ballotBoxesIssued"):
                tallySheetVersionRow.add_issued_ballot_box(issued_ballot_box_id)

            for received_ballot_box_id in party_count_body.get("ballotBoxesReceived"):
                tallySheetVersionRow.add_received_ballot_box(received_ballot_box_id)

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data

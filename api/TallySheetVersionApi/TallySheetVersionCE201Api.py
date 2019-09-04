from app import db
from util import RequestBody
from schemas import TallySheetVersionCE201Schema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionCE201
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersionCE201.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionCE201Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersionCE201.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersionCE201Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersion = TallySheetVersionCE201.create(
        tallySheetId=tallySheetId
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
                boxCountOrdinary=party_count_body.get("boxCountOrdinary"),
                boxCountTendered=party_count_body.get("boxCountTendered"),
                ballotPaperAccountOrdinary=party_count_body.get("ballotPaperAccountOrdinary"),
                ballotPaperAccountTendered=party_count_body.get("ballotPaperAccountTendered")
            )

            for issued_ballot_body in party_count_body.get("issuedBallots"):
                issued_ballot_body = RequestBody(issued_ballot_body)
                tallySheetVersionRow.add_issued_ballot_box(issued_ballot_body.get("stationaryItemId"))

            for received_ballot_body in party_count_body.get("receivedBallots"):
                received_ballot_body = RequestBody(received_ballot_body)
                tallySheetVersionRow.add_received_ballot_box(received_ballot_body.get("stationaryItemId"))

    db.session.commit()

    return TallySheetVersionCE201Schema().dump(tallySheetVersion).data

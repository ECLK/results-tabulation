from util import RequestBody
from schemas import TallySheetVersionPRE201Schema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionCE201
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersionCE201.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE201Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersionCE201.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersionPRE201Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersion = TallySheetVersionCE201.create(
        tallySheetId=tallySheetId
    )

    tally_sheet_content = request_body.get("tallySheetContent")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            tallySheetVersion.add_row(
                areaId=party_count_body.get("areaId"),
                issuedBallotCount=party_count_body.get("issuedBallotCount"),
                issuedTenderBallotCount=party_count_body.get("issuedTenderBallotCount"),
                receivedBallotCount=party_count_body.get("receivedBallotCount"),
                receivedTenderBallotCount=party_count_body.get("receivedTenderBallotCount")
            )

    return TallySheetVersionPRE201Schema().dump(tallySheetVersion).data

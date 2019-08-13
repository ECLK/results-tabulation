from util import RequestBody
from schemas import TallySheetVersionPRE41Schema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.entities.Result.PartyWiseResult import PartyCount
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersionPRE41.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE41Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersionPRE41.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersionPRE41Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    pre41 = TallySheetVersionPRE41.create(
        tallySheetId=tallySheetId
    )

    tally_sheet_content = request_body.get("tallySheetContent")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            PartyCount.create(
                partyWiseResultId=pre41.partyWiseResultId,
                partyId=party_count_body.get("partyId"),
                count=party_count_body.get("count"),
                countInWords=party_count_body.get("countInWords"),
                electionId=pre41.submission.electionId
            )

    return TallySheetVersionPRE41Schema().dump(pre41).data

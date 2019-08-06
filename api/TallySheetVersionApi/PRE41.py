from util import RequestBody
from schemas import Ballot_Schema as Schema, TallySheetVersionPRE41Schema
from orm.entities import TallySheetVersion, TallySheet
from orm.entities.TallySheetVersion import PRE41
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.enums import TallySheetCodeEnum
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = PRE41.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE41Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = PRE41.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersionPRE41Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    pre41 = PRE41.create(
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
                countInWords=party_count_body.get("countInWords")
                # electionId=pre41.tallySheet.electionId
            )

    return TallySheetVersionPRE41Schema().dump(pre41).data

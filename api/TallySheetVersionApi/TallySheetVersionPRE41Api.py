from util import RequestBody
from schemas import TallySheetVersionPRE41Schema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersionPRE41.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    print("\n\n\n ####### result ##### ", result)

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
    tallySheetVersion = TallySheetVersionPRE41.create(
        tallySheetId=tallySheetId
    )

    tally_sheet_content = request_body.get("tallySheetContent")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            tallySheetVersion.add_row(
                candidateId=party_count_body.get("candidateId"),
                count=party_count_body.get("count"),
                countInWords=party_count_body.get("countInWords")
            )

    return TallySheetVersionPRE41Schema().dump(tallySheetVersion).data

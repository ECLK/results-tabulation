from app import db
from util import RequestBody
from schemas import TallySheetVersion_CE_201_PV_Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_CE_201_PV
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion_CE_201_PV.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_CE_201_PV_Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersion_CE_201_PV.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersion_CE_201_PV_Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersion = TallySheetVersion_CE_201_PV.create(
        tallySheetId=tallySheetId
    )

    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            tallySheetVersion.add_row(
                count=party_count_body.get("count"),
                invalidVoteCategoryId=party_count_body.get("invalidVoteCategoryId")
            )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data

from orm.entities.Submission.TallySheet import Model as TallySheetModel
from schemas import TallySheetSchema

from schemas import TallySheetSchema as Schema
from orm.entities.Submission import TallySheet


def getAll(electionId=None, officeId=None, tallySheetCode=None):
    result = TallySheet.get_all(
        electionId=electionId,
        officeId=officeId,
        tallySheetCode=tallySheetCode
    )

    return Schema(many=True).dump(result).data


def get_by_id(tallySheetId):
    tallySheet = TallySheetModel.query.filter(TallySheetModel.tallySheetId == tallySheetId).one_or_none()

    return TallySheetSchema().dump(tallySheet).data


def get_tallysheet_response(new_tallysheet):
    if new_tallysheet.code == "PRE-41":
        return TallySheetSchema().dump(new_tallysheet).data
    else:
        return TallySheetSchema().dump(new_tallysheet).data

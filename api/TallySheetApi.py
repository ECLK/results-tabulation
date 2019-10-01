from typing import Set

from auth import get_user_access_area_ids, authorize
from auth.AuthConstants import ALL_ROLES
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import Model as TallySheetModel
from schemas import TallySheetSchema
from schemas import TallySheetSchema as Schema


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, officeId=None, tallySheetCode=None):
    result = TallySheet.get_all(
        electionId=electionId,
        officeId=officeId,
        tallySheetCode=tallySheetCode
    )

    # filter results based on user's access to areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()
    filtered_result = []
    tally_sheet: TallySheetModel
    for tally_sheet in result:
        if tally_sheet.officeId in user_access_area_ids:
            filtered_result.append(tally_sheet)

    return Schema(many=True).dump(filtered_result).data


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId):
    tallySheet = TallySheetModel.query.filter(TallySheetModel.tallySheetId == tallySheetId).one_or_none()

    return TallySheetSchema().dump(tallySheet).data


def get_tallysheet_response(new_tallysheet):
    if new_tallysheet.code == "PRE-41":
        return TallySheetSchema().dump(new_tallysheet).data
    else:
        return TallySheetSchema().dump(new_tallysheet).data

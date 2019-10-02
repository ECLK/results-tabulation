from typing import Set

from auth import authorize
from auth.AuthConstants import ALL_ROLES
from exception import NotFoundException
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import Model as TallySheetModel
from schemas import TallySheetSchema


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, officeId=None, tallySheetCode=None):
    result = TallySheet.get_all(
        electionId=electionId,
        officeId=officeId,
        tallySheetCode=tallySheetCode
    )

    return TallySheetSchema(many=True).dump(result).data


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId):
    tally_sheet = TallySheetModel.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    return TallySheetSchema().dump(tally_sheet).data

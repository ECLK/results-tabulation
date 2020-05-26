import {
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_34_CO,
    TALLY_SHEET_CODE_PRE_41
} from "../TALLY_SHEET_CODE";
import TallySheetEdit_PRE_41 from "./tally-sheet-edit-pre-41";
import TallySheetEdit_PRE_34_CO from "./tally-sheet-edit-pre-34-co";
import TallySheetEdit_CE_201_PV from "./tally-sheet-edit-ce-201-pv";
import TallySheetEdit from "../../../../tally-sheet/tally-sheet-edit";

export default class PresidentialElection2019TallySheetEdit extends TallySheetEdit {
    getTallySheetEditForm(tallySheetCode) {
        if (tallySheetCode === TALLY_SHEET_CODE_PRE_41) {
            return TallySheetEdit_PRE_41
        } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_34_CO) {
            return TallySheetEdit_PRE_34_CO
        } else {
            return super.getTallySheetEditForm(tallySheetCode)
        }
    }
}

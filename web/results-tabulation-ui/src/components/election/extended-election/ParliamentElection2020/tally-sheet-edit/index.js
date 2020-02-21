import TallySheetEdit from "../../../../tally-sheet/tally-sheet-edit";
import {TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_4} from "../TALLY_SHEET_CODE";
import TallySheetEdit_PE_27 from "./tally-sheet-edit-pe-27";
import TallySheetEdit_PE_4 from "./tally-sheet-edit-pe-4";

export default class ParliamentElection2020TallySheetEdit extends TallySheetEdit {
    getTallySheetEditForm(tallySheetCode) {
        if (tallySheetCode === TALLY_SHEET_CODE_PE_27) {
            return TallySheetEdit_PE_27
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_4) {
            return TallySheetEdit_PE_4
        } else {
            return super.getTallySheetEditForm(tallySheetCode)
        }
    }
}

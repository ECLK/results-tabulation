import TallySheetEdit from "../../../../tally-sheet/tally-sheet-edit";
import {
    TALLY_SHEET_CODE_PE_27,
    TALLY_SHEET_CODE_PE_4,
    TALLY_SHEET_CODE_PE_39,
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_PE_R2, TALLY_SHEET_CODE_PE_21, TALLY_SHEET_CODE_PE_AI_NL_1, TALLY_SHEET_CODE_PE_AI_NL_2
} from "../TALLY_SHEET_CODE";
import TallySheetEdit_PE_27 from "./tally-sheet-edit-pe-27";
import TallySheetEdit_PE_4 from "./tally-sheet-edit-pe-4";
import TallySheetEdit_PE_39 from "./tally-sheet-edit-pe-39";
import TallySheetEdit_PE_22 from "./tally-sheet-edit-pe-22";
import TallySheetEdit_PE_R2 from "./tally-sheet-edit-pe-r2";
import TallySheetEdit_PE_21 from "./tally-sheet-edit-pe-21";
import TallySheetEdit_PE_AI_NL_1 from "./tally-sheet-edit-pe-ai-nl-1";
import TallySheetEdit_PE_AI_NL_2 from "./tally-sheet-edit-pe-ai-nl-2";

export default class ParliamentElection2020TallySheetEdit extends TallySheetEdit {
    getTallySheetEditForm(tallySheetCode) {
        if (tallySheetCode === TALLY_SHEET_CODE_PE_27) {
            return TallySheetEdit_PE_27
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_4) {
            return TallySheetEdit_PE_4
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_39) {
            return TallySheetEdit_PE_39
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_22) {
            return TallySheetEdit_PE_22
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_R2) {
            return TallySheetEdit_PE_R2
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_21) {
            return TallySheetEdit_PE_21
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_AI_NL_1) {
            return TallySheetEdit_PE_AI_NL_1
        } else if (tallySheetCode === TALLY_SHEET_CODE_PE_AI_NL_2) {
            return TallySheetEdit_PE_AI_NL_2
        } else {
            return super.getTallySheetEditForm(tallySheetCode)
        }
    }
}

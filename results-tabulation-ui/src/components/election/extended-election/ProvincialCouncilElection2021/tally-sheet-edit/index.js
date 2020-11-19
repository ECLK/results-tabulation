import TallySheetEdit from "../../../../tally-sheet/tally-sheet-edit";
import {
    TALLY_SHEET_CODE_PCE_35,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_4,
    TALLY_SHEET_CODE_PCE_34,
    TALLY_SHEET_CODE_PCE_31,
    TALLY_SHEET_CODE_PCE_R2, TALLY_SHEET_CODE_PCE_42, TALLY_SHEET_CODE_PCE_PC_BS_1, TALLY_SHEET_CODE_PCE_PC_BS_2
} from "../TALLY_SHEET_CODE";
import TallySheetEdit_PCE_35 from "./tally-sheet-edit-pce-35";
import TallySheetEdit_PCE_CE_CO_PR_4 from "./tally-sheet-edit-pce-ce-co-pr-4";
import TallySheetEdit_PCE_34 from "./tally-sheet-edit-pce-34";
import TallySheetEdit_PCE_31 from "./tally-sheet-edit-pce-31";
import TallySheetEdit_PCE_R2 from "./tally-sheet-edit-pce-r2";
import TallySheetEdit_PCE_42 from "./tally-sheet-edit-pce-42";
import TallySheetEdit_PCE_PC_BS_1 from "./tally-sheet-edit-pce-pc-bs-1";
import TallySheetEdit_PCE_PC_BS_2 from "./tally-sheet-edit-pce-pc-bs-2";

export default class ProvincialCouncilElection2021TallySheetEdit extends TallySheetEdit {
    getTallySheetEditForm(tallySheetCode) {
        if (tallySheetCode === TALLY_SHEET_CODE_PCE_35) {
            return TallySheetEdit_PCE_35
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_CE_CO_PR_4) {
            return TallySheetEdit_PCE_CE_CO_PR_4
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_34) {
            return TallySheetEdit_PCE_34
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_31) {
            return TallySheetEdit_PCE_31
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_R2) {
            return TallySheetEdit_PCE_R2
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_42) {
            return TallySheetEdit_PCE_42
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_PC_BS_1) {
            return TallySheetEdit_PCE_PC_BS_1
        } else if (tallySheetCode === TALLY_SHEET_CODE_PCE_PC_BS_2) {
            return TallySheetEdit_PCE_PC_BS_2
        } else {
            return super.getTallySheetEditForm(tallySheetCode)
        }
    }
}

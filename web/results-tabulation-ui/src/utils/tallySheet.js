import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_34_ED,
} from "../components/election/extended-election/PresidentialElection2019/TALLy_SHEET_CODES";
import {VOTE_TYPE_POSTAL} from "../components/election/constants/VOTE_TYPE";

export function getTallySheetCodeStr({tallySheetCode, election}) {
    let tallySheetCodeStr = tallySheetCode;

    if (tallySheetCode === TALLY_SHEET_CODE_PRE_34_PD) {
        tallySheetCodeStr = "REVISED-30-PD"
    }
    if (tallySheetCode === TALLY_SHEET_CODE_PRE_34_ED) {
        tallySheetCodeStr = "REVISED-30-ED"
    }
    if (tallySheetCode && election && election.voteType === VOTE_TYPE_POSTAL) {
        if (tallySheetCode === TALLY_SHEET_CODE_CE_201_PV || tallySheetCode === TALLY_SHEET_CODE_CE_201) {
            tallySheetCodeStr = tallySheetCode
        } else {
            tallySheetCodeStr = tallySheetCode + "-PV"
        }
    }

    return tallySheetCodeStr;
}

export function getAreaName(area) {
    let areaName = null;
    if (area) {
        areaName = area.areaName;
    }

    return areaName;
}

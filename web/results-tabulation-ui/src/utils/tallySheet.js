import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_34_ED,
} from "../components/election/election-menu/PRESIDENTIAL_ELECTION_2019/TALLy_SHEET_CODES";
import {VOTE_TYPE_POSTAL} from "../components/election/constants/VOTE_TYPE";

export const getPollingDivisionName = (tallySheet) => {
    let pollingDivisionName = null;
    if (tallySheet) {
        const {pollingDivisions} = tallySheet.area;
        if (pollingDivisions.length > 0) {
            const {areaName} = pollingDivisions[0];
            pollingDivisionName = areaName;
        }
    }

    return pollingDivisionName;
};

export const getElectoralDistrictName = (tallySheet) => {
    let electoralDistrictName = null;
    if (tallySheet) {
        const {electoralDistricts} = tallySheet.area;
        if (electoralDistricts.length > 0) {
            const {areaName} = electoralDistricts[0];
            electoralDistrictName = areaName;
        }
    }

    return electoralDistrictName;
};

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

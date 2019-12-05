import {VOTE_TYPE} from "../services/tabulation-api/entities/election.entity";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_PD,
    TALLY_SHEET_CODE_PRE_30_PV,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_34_ED,
} from "../App";

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
    if (tallySheetCode && election && election.voteType === VOTE_TYPE.POSTAL) {
        if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_PD) {
            tallySheetCodeStr = TALLY_SHEET_CODE_PRE_30_PV
        } else if (tallySheetCode === TALLY_SHEET_CODE_CE_201_PV || tallySheetCode === TALLY_SHEET_CODE_CE_201) {
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
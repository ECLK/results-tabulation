import {
    WORKFLOW_STATUS_TYPE_EMPTY,
    WORKFLOW_STATUS_TYPE_RELEASED,
    WORKFLOW_STATUS_TYPE_SAVED
} from "./WORKFLOW_STATUS_TYPE";

export const TALLY_SHEET_LIST_COLUMN_STATUS = "TALLY_SHEET_LIST_COLUMN_STATUS";
export const TALLY_SHEET_LIST_COLUMN_ACTIONS = "TALLY_SHEET_LIST_COLUMN_ACTIONS";
export const TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT = "TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT";
export const TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION = "TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION";
export const TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE = "TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE";
export const TALLY_SHEET_LIST_COLUMN_COUNTRY = "TALLY_SHEET_LIST_COLUMN_COUNTRY";
export const TALLY_SHEET_LIST_COLUMN_PARTY = "TALLY_SHEET_LIST_COLUMN_PARTY";

export const TALLY_SHEET_LIST_COLUMN_LABEL = {
    [TALLY_SHEET_LIST_COLUMN_STATUS]: "Status",
    [TALLY_SHEET_LIST_COLUMN_ACTIONS]: "Actions",
    [TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT]: "Electoral District",
    [TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION]: "Polling Division",
    [TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE]: "Counting Centre",
    [TALLY_SHEET_LIST_COLUMN_COUNTRY]: "Country",
    [TALLY_SHEET_LIST_COLUMN_PARTY]: "Party"
};

export const TALLY_SHEET_LIST_COLUMN_VALUE = {
    [TALLY_SHEET_LIST_COLUMN_STATUS]: (tallySheet) => {
        if (tallySheet.template.isDerived & [WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED].indexOf(
            tallySheet.workflowInstance.status) >= 0) {

            return "Not Verified";
        } else {

            return tallySheet.workflowInstance.status
        }
    },
    [TALLY_SHEET_LIST_COLUMN_ACTIONS]: (tallySheet) => tallySheet["actions"],
    [TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT]: (tallySheet) => tallySheet["electoralDistrictName"],
    [TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION]: (tallySheet) => tallySheet["pollingDivisionName"],
    [TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE]: (tallySheet) => tallySheet["countingCentreName"],
    [TALLY_SHEET_LIST_COLUMN_COUNTRY]: (tallySheet) => tallySheet["countryName"],
    [TALLY_SHEET_LIST_COLUMN_PARTY]: (tallySheet) => {
        return tallySheet.election.partyMap[tallySheet.metaDataMap["partyId"]].partyName;
    },
};

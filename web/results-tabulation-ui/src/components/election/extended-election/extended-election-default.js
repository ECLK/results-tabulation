import React from "react";
import TallySheetEdit from "../../tally-sheet/tally-sheet-edit";
import {getFirstOrNull} from "../../../utils";

export default class ExtendedElectionDefault {
    TALLY_SHEET_LIST_COLUMNS = {};
    TALLY_SHEET_LIST_ACTIONS = {};
    election = null;
    TallySheetEditComponent = TallySheetEdit;

    constructor(election, TALLY_SHEET_LIST_COLUMNS = {}, TALLY_SHEET_LIST_ACTIONS = {}, TallySheetEditComponent = null) {
        this.election = election;
        this.TALLY_SHEET_LIST_COLUMNS = TALLY_SHEET_LIST_COLUMNS;
        this.TALLY_SHEET_LIST_ACTIONS = TALLY_SHEET_LIST_ACTIONS;

        if (TallySheetEditComponent) {
            this.TallySheetEditComponent = TallySheetEditComponent;
        }
    }

    getElectionHome() {
        return <div>TODO: Define the default election template.</div>
    }

    async mapRequiredAreasToTallySheet(tallySheet) {
        const {areaMapList} = tallySheet;
        const firstAreaMap = getFirstOrNull(areaMapList);
        if (firstAreaMap) {
            const {
                countingCentreName = "", pollingDivisionName = "", electoralDistrictName = "", countryName = ""
            } = firstAreaMap;
            Object.assign(tallySheet, {countingCentreName, pollingDivisionName, electoralDistrictName, countryName});
        }

        return tallySheet;
    }

    getTallySheetListColumns(tallySheetCode, voteType) {
        if (this.TALLY_SHEET_LIST_COLUMNS[tallySheetCode]) {
            return this.TALLY_SHEET_LIST_COLUMNS[tallySheetCode][voteType];
        } else {
            return null;
        }
    }

    getTallySheetListActions(tallySheetCode, voteType) {
        if (this.TALLY_SHEET_LIST_ACTIONS[tallySheetCode]) {
            return this.TALLY_SHEET_LIST_ACTIONS[tallySheetCode][voteType];
        } else {
            return null;
        }
    }
}

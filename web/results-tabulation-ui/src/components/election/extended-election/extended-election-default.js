import React from "react";
import TallySheetEdit from "../../tally-sheet/tally-sheet-edit";

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

    mapRequiredAreasToTallySheet(tallySheet) {
        return tallySheet
    }

    getTallySheetListColumns(tallySheetCode) {
        const {voteType} = this.election;

        if (this.TALLY_SHEET_LIST_COLUMNS[tallySheetCode]) {
            return this.TALLY_SHEET_LIST_COLUMNS[tallySheetCode][voteType];
        } else {
            return null;
        }
    }

    getTallySheetListActions(tallySheetCode) {
        const {voteType} = this.election;

        if (this.TALLY_SHEET_LIST_ACTIONS[tallySheetCode]) {
            return this.TALLY_SHEET_LIST_ACTIONS[tallySheetCode][voteType];
        } else {
            return null;
        }
    }

}

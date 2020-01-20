import React from "react";
import TallySheetListRowActionView from "./tally-sheet-list-row-action-view";
import TallySheetListRowActionEnter from "./tally-sheet-list-row-action-enter";
import TallySheetListRowActionEdit from "./tally-sheet-list-row-action-edit";
import TallySheetListRowActionVerify from "./tally-sheet-list-row-action-verify";
import TallySheetListRowActionUnlock from "./tally-sheet-list-row-action-unlock";

export const TALLY_SHEET_LIST_ROW_ACTION = {
    TALLY_SHEET_LIST_ROW_ACTION_ENTER: "TALLY_SHEET_LIST_ROW_ACTION_ENTER",
    TALLY_SHEET_LIST_ROW_ACTION_EDIT: "TALLY_SHEET_LIST_ROW_ACTION_EDIT",
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY: "TALLY_SHEET_LIST_ROW_ACTION_VERIFY",
    TALLY_SHEET_LIST_ROW_ACTION_VIEW: "TALLY_SHEET_LIST_ROW_ACTION_VIEW",
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK: "TALLY_SHEET_LIST_ROW_ACTION_UNLOCK",
};


export default function TallySheetListRowAction({history, action, electionId, tallySheetListRow}) {
    switch (action) {
        case TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_ENTER:
            return <TallySheetListRowActionEnter history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_EDIT:
            return <TallySheetListRowActionEdit history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VERIFY:
            return <TallySheetListRowActionVerify history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VIEW:
            return <TallySheetListRowActionView history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_UNLOCK:
            return <TallySheetListRowActionUnlock history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;

    }
}



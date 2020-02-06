import React from "react";
import TallySheetListRowActionView from "./tally-sheet-list-row-action-view";
import TallySheetListRowActionEnterOrEdit from "./tally-sheet-list-row-action-enter-or-edit";
import TallySheetListRowActionRequestEdit from "./tally-sheet-list-row-action-request-edit";
import TallySheetListRowActionVerify from "./tally-sheet-list-row-action-verify";
import TallySheetListRowActionUnlock from "./tally-sheet-list-row-action-unlock";
import {
    TALLY_SHEET_LIST_ROW_ACTION_ENTER_OR_EDIT,
    TALLY_SHEET_LIST_ROW_ACTION_REQUEST_EDIT,
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
    TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../../constants/TALLY_SHEET_ACTION";


export default function TallySheetListRowAction({history, action, electionId, tallySheetListRow}) {
    switch (action) {
        case TALLY_SHEET_LIST_ROW_ACTION_ENTER_OR_EDIT:
            return <TallySheetListRowActionEnterOrEdit history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION_REQUEST_EDIT:
            return <TallySheetListRowActionRequestEdit history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION_VERIFY:
            return <TallySheetListRowActionVerify history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION_VIEW:
            return <TallySheetListRowActionView history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;
        case TALLY_SHEET_LIST_ROW_ACTION_UNLOCK:
            return <TallySheetListRowActionUnlock history={history} electionId={electionId} tallySheetListRow={tallySheetListRow}/>;

    }

    return null
}



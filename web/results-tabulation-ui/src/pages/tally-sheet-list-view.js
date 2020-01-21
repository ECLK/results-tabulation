import React from "react";
import TallySheetList from "../components/tally-sheet/tally-sheet-list";
import {getTallySheetListActions, getTallySheetListColumns} from "../components/election/election-menu";


export default function TallySheetListView({history, queryString, election}) {
    const {tallySheetCode} = queryString;

    const props = {history, election, tallySheetCode};

    const columns = getTallySheetListColumns(election, tallySheetCode);
    if (columns) {
        props.columns = columns
    }

    const actions = getTallySheetListActions(election, tallySheetCode);
    if (actions) {
        props.actions = actions
    }

    return <TallySheetList
        {...props}
    />;
}

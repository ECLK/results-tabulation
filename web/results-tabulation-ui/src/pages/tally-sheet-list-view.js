import React from "react";
import TallySheetList from "../components/tally-sheet/tally-sheet-list";
import ExtendedElection from "../components/election/extended-election";


export default function TallySheetListView({history, queryString, election}) {
    const extendedElection = ExtendedElection(election);
    const {tallySheetCode} = queryString;

    const props = {history, election, tallySheetCode};

    const columns = extendedElection.getTallySheetListColumns(tallySheetCode);
    if (columns) {
        props.columns = columns
    }

    const actions = extendedElection.getTallySheetListActions(tallySheetCode);
    if (actions) {
        props.actions = actions
    }

    return <TallySheetList
        {...props}
    />;
}

import React from "react";
import TallySheetList from "../components/tally-sheet/tally-sheet-list";
import ExtendedElection from "../components/election/extended-election";
import TabulationPage from "./index";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import {PATH_ELECTION_TALLY_SHEET_LIST} from "../App";


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

    const additionalBreadCrumbLinks = [
        {
            label: getTallySheetCodeStr({tallySheetCode, election: election}).toLowerCase(),
            to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode)
        }
    ];

    return <TabulationPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}>
        <TallySheetList
            {...props}
        />
    </TabulationPage>
}

import React from "react";
import TallySheetList from "../components/tally-sheet/tally-sheet-list";
import ExtendedElection from "../components/election/extended-election";
import TabulationPage from "./index";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import {PATH_ELECTION_TALLY_SHEET_LIST} from "../App";


export default function TallySheetListView({history, queryString, election}) {
    const extendedElection = ExtendedElection(election);
    const {tallySheetCode, voteType, partyId} = queryString;

    const props = {history, election, tallySheetCode, voteType, partyId};

    const columns = extendedElection.getTallySheetListColumns(tallySheetCode, voteType);
    if (columns) {
        props.columns = columns
    }

    const additionalBreadCrumbLinks = [];

    if (partyId) {
        const party = election.partyMap[partyId];
        additionalBreadCrumbLinks.push({
            label: getTallySheetCodeStr({tallySheetCode, voteType}) + " - " + party.partyName.toLowerCase(),
            to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType, partyId)
        });
    } else {
        additionalBreadCrumbLinks.push({
            label: getTallySheetCodeStr({tallySheetCode, voteType}),
            to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType)
        });
    }


    return <TabulationPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}>
        <TallySheetList
            {...props}
        />
    </TabulationPage>
}

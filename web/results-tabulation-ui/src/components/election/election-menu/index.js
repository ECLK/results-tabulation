import React from "react";
import * as PRESIDENTIAL_ELECTION_2019 from "./PRESIDENTIAL_ELECTION_2019";
import * as PARLIAMENT_ELECTION_2020 from "./PARLIAMENT_ELECTION_2020";

const ELECTION_TEMPLATE_NAME = {
    PRESIDENTIAL_ELECTION_2019: "PRESIDENTIAL_ELECTION_2019",
    PARLIAMENT_ELECTION_2020: "PARLIAMENT_ELECTION_2020"
};


export const ElectionHome = function ({election}) {
    const extendedElection = getExtendedElection(election);

    return <extendedElection.ElectionHome election={election}/>;
}

export function getExtendedElection(election) {
    const {electionTemplateName} = election;
    let extendedElection = null;

    switch (electionTemplateName) {
        case ELECTION_TEMPLATE_NAME.PRESIDENTIAL_ELECTION_2019:
            extendedElection = PRESIDENTIAL_ELECTION_2019;
            break;
        case ELECTION_TEMPLATE_NAME.PARLIAMENT_ELECTION_2020:
            extendedElection = PARLIAMENT_ELECTION_2020;
            break;
        default:
            throw Error(`Election template is not defined. [${electionTemplateName}]`)
    }

    return extendedElection;
}

export function mapRequiredAreasToTallySheet(tallySheet) {
    const extendedElection = getExtendedElection(tallySheet.election.rootElection);

    return extendedElection.mapRequiredAreasToTallySheet(tallySheet);
}

export function getTallySheetListColumns(election, tallySheetCode) {
    const {voteType} = election;
    const extendedElection = getExtendedElection(election.rootElection);

    if (extendedElection.TALLY_SHEET_LIST_COLUMNS[tallySheetCode]) {
        return extendedElection.TALLY_SHEET_LIST_COLUMNS[tallySheetCode][voteType];
    } else {
        return null;
    }
}

export function getTallySheetListActions(election, tallySheetCode) {
    const {voteType} = election;
    const extendedElection = getExtendedElection(election.rootElection);

    if (extendedElection.TALLY_SHEET_LIST_ACTIONS[tallySheetCode]) {
        return extendedElection.TALLY_SHEET_LIST_ACTIONS[tallySheetCode][voteType];
    } else {
        return null;
    }
}

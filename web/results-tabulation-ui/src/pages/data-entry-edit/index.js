import React from "react";
import {
    PATH_ELECTION, PATH_ELECTION_BY_ID,
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
} from "../../App";
import BreadCrumb from "../../components/bread-crumb";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import ExtendedElection from "../../components/election/extended-election";


export default function DataEntryEdit({history, queryString, election, tallySheet, messages}) {
    const {tallySheetCode} = tallySheet;
    const {electionId, rootElection} = election;

    function getEditorJsx() {
        const props = {history, queryString, election, tallySheet, messages};
        const extendedElection = ExtendedElection(election);

        return <extendedElection.TallySheetEditComponent {...props}/>
    }

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: rootElection.electionName, to: PATH_ELECTION_BY_ID(rootElection.electionId)},
                {
                    label: getTallySheetCodeStr(tallySheet).toLowerCase(),
                    to: PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode)
                },
                {
                    label: tallySheet.area.areaName,
                    to: PATH_ELECTION_TALLY_SHEET_VIEW(electionId, tallySheet.tallySheetId)
                },
            ]}
        />
        <div className="page-content">
            <div className="data-entry-edit-header">
                <div className="data-entry-edit-header-election-name">{rootElection.electionName}</div>
                <div className="data-entry-edit-header-tally-sheet-code">{getTallySheetCodeStr(tallySheet)}</div>
            </div>
            <div>{tallySheet.electoralDistrict ? 'Electoral District: ' + tallySheet.electoralDistrict.areaName : null}
                {tallySheet.pollingDivision ? ' > Polling Division: ' + tallySheet.pollingDivision.areaName : null}
                {tallySheet.countingCentre ? ' > Counting Centre: ' + tallySheet.countingCentre.areaName : null}</div>
            {getEditorJsx()}
        </div>
    </div>
}

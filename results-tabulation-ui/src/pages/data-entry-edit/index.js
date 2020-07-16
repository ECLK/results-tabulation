import React, {useContext} from "react";
import {
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
} from "../../App";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import ExtendedElection from "../../components/election/extended-election";
import {TabulationTallySheetPage} from "../index";
import {TallySheetContext} from "../../services/tally-sheet.provider";


export default function DataEntryEdit({history, queryString, election, tallySheetId}) {
    const tallySheetContext = useContext(TallySheetContext);
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const {tallySheetCode, metaDataMap} = tallySheet;
    const {electionId, voteType} = election;
    const additionalBreadCrumbLinks = [
        {
            label: getTallySheetCodeStr({tallySheetCode, voteType}).toLowerCase(),
            to: PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)
        }
    ];

    if (metaDataMap.partyId && election.partyMap[metaDataMap.partyId]) {
        // Map the parties to the breadcrumb.
        const party = election.partyMap[metaDataMap.partyId];
        const {partyName} = party;
        additionalBreadCrumbLinks.push({
            label: `${tallySheet.area.areaName} - ${partyName}`,
            to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
        })
    } else {
        additionalBreadCrumbLinks.push({
            label: tallySheet.area.areaName,
            to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
        })
    }

    function getEditorJsx() {
        const props = {history, queryString, election, tallySheet};
        const extendedElection = ExtendedElection(election);

        return <extendedElection.TallySheetEditComponent {...props}/>
    }

    return <TabulationTallySheetPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}
                                     tallySheet={tallySheet} history={history}>
        <div className="page-content">
            <div>{tallySheet.electoralDistrict ? 'Electoral District: ' + tallySheet.electoralDistrict.areaName : null}
                {tallySheet.pollingDivision ? ' > Polling Division: ' + tallySheet.pollingDivision.areaName : null}
                {tallySheet.countingCentre ? ' > Counting Centre: ' + tallySheet.countingCentre.areaName : null}</div>
            {getEditorJsx()}
        </div>
    </TabulationTallySheetPage>
}

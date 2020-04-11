import React, {useContext} from "react";
import {
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
} from "../../App";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import ExtendedElection from "../../components/election/extended-election";
import {TabulationTallySheetPage} from "../index";
import {TallySheetContext} from "../../services/tally-sheet.provider";


export default function DataEntryEdit({history, queryString, election, tallySheetId, messages}) {
    const tallySheetContext = useContext(TallySheetContext);
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const {tallySheetCode} = tallySheet;
    const {electionId, rootElection, voteType} = election;
    const additionalBreadCrumbLinks = [
        {
            label: getTallySheetCodeStr({tallySheetCode, voteType}).toLowerCase(),
            to: PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)
        },
        {
            label: tallySheet.area.areaName,
            to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
        }
    ];

    function getEditorJsx() {
        const props = {history, queryString, election, tallySheet, messages};
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

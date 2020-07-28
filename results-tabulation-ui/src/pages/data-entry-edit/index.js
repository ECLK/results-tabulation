import React, {useContext} from "react";
import {
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
} from "../../App";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import ExtendedElection from "../../components/election/extended-election";
import {TabulationTallySheetPage} from "../index";
import {TallySheetContext} from "../../services/tally-sheet.provider";
import {
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_CE_RO_PR_1
} from "../../components/election/extended-election/ParliamentElection2020/TALLY_SHEET_CODE";


export default function DataEntryEdit({history, queryString, election, tallySheetId}) {
    const tallySheetContext = useContext(TallySheetContext);
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const {tallySheetCode, metaDataMap} = tallySheet;
    const {electionId, voteType} = election;
    let additionalBreadCrumbLinks;

    if (metaDataMap["partyId"]) {
        const partyId = metaDataMap["partyId"];
        const party = election.partyMap[partyId];

        if ([TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22, TALLY_SHEET_CODE_PE_CE_RO_PR_1].indexOf(tallySheetCode) >= 0) {
            additionalBreadCrumbLinks = [{
                label: getTallySheetCodeStr({tallySheetCode, voteType}) + " - " + party.partyName.toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType, partyId)
            }, {
                label: tallySheet.area.areaName.toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
            }];
        } else {
            additionalBreadCrumbLinks = [{
                label: getTallySheetCodeStr({tallySheetCode, voteType}),
                to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType)
            }, {
                label: (party.partyName + " - " + tallySheet.area.areaName).toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
            }];
        }
    } else {
        additionalBreadCrumbLinks = [{
            label: getTallySheetCodeStr({tallySheetCode, voteType}),
            to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType)
        }, {
            label: tallySheet.area.areaName.toLowerCase(),
            to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
        }];
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

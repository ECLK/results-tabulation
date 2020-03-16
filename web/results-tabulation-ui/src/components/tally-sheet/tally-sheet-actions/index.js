import React from "react";
import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../App";
import {executeTallySheetWorkflow} from "../../../services/tabulation-api";
import Button from "@material-ui/core/Button";


export default function TallySheetActions({tallySheet, electionId, history, onTallySheetUpdate}) {
    return tallySheet.workflowInstance.actions.filter((action) => {
        return action.allowed;
    }).map((action, actionIndex) => {
        return <Button
            variant="outlined" color="default"
            size="small"
            onClick={async () => {

                if (action.actionType === "SAVE") {
                    history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                } else {
                    const _tallySheet = await executeTallySheetWorkflow(tallySheet.tallySheetId, action.workflowActionId);
                    onTallySheetUpdate && onTallySheetUpdate(_tallySheet);

                    if (action.actionType === "EDIT") {
                        history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                    } else if (action.actionType === "VIEW") {
                        history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                    }
                }
            }}
        >
            {action.actionName}
        </Button>
    });
}

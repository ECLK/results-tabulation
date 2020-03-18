import React, {useContext} from "react";
import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../App";
import Button from "@material-ui/core/Button";
import {TallySheetContext} from "../../../services/tally-sheet.provider";


export default function TallySheetActions({tallySheetId, electionId, history}) {
    const tallySheetContext = useContext(TallySheetContext);

    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    return tallySheet.workflowInstance.actions.filter((action) => {
        return action.allowed;
    }).map((action, actionIndex) => {
        return <Button
            key={actionIndex}
            variant="outlined" color="default"
            size="small"
            onClick={async () => {

                if (action.actionType === "SAVE") {
                    history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                } else {
                    await tallySheetContext.executeTallySheetWorkflow(tallySheet.tallySheetId, action.workflowActionId);

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

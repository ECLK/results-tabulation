import React, {useContext} from "react";
import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../App";
import Button from "@material-ui/core/Button";
import {TallySheetContext} from "../../../services/tally-sheet.provider";
import {
    WORKFLOW_ACTION_TYPE_EDIT,
    WORKFLOW_ACTION_TYPE_SAVE,
    WORKFLOW_ACTION_TYPE_VIEW
} from "../constants/WORKFLOW_ACTION_TYPE";


export default function TallySheetActions({tallySheetId, electionId, history, filter}) {
    const tallySheetContext = useContext(TallySheetContext);

    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    return tallySheet.workflowInstance.actions.filter((action) => {
        if (action.allowed) {
            if (filter) {
                return filter(action);
            } else {
                return true;
            }
        } else {
            return false;
        }
    }).map((action, actionIndex) => {
        return <Button
            key={actionIndex}
            variant="outlined" color="default"
            size="small"
            disabled={!action.authorized}
            onClick={async () => {
                if (action.actionType !== WORKFLOW_ACTION_TYPE_VIEW) {
                    if (tallySheet.template.isDerived || action.actionType !== WORKFLOW_ACTION_TYPE_SAVE) {
                        await tallySheetContext.executeTallySheetWorkflow(tallySheet.tallySheetId, action.workflowActionId);
                    }
                }


                if ([
                    WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_EDIT, WORKFLOW_ACTION_TYPE_SAVE
                ].indexOf(action.actionType) >= 0) {
                    history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                }
            }}
        >
            {action.actionName}
        </Button>
    });
}

import React from "react";
import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../../App";
import Button from "@material-ui/core/Button";
import {executeTallySheetWorkflow} from "../../../../services/tabulation-api";


export default function TallySheetListRowAction({history, action, electionId, tallySheetListRow, onTallySheetUpdate}) {

    return <Button
        variant="outlined" color="default"
        size="small"
        onClick={async () => {

            if (action.actionType === "SAVE") {
                history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetListRow.tallySheetId))
            } else {
                const tallySheet = await executeTallySheetWorkflow(tallySheetListRow.tallySheetId, action.workflowActionId);
                onTallySheetUpdate && onTallySheetUpdate(tallySheet);

            }
        }}
    >
        {action.actionName}
    </Button>

}



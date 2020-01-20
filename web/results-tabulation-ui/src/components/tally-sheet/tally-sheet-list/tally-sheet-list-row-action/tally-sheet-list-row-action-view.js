import {PATH_ELECTION_DATA_ENTRY_EDIT, PATH_ELECTION_REPORT_VIEW} from "../../../../App";
import Button from "@material-ui/core/Button";
import React from "react";

export default function TallySheetListRowActionView({history, electionId, tallySheetListRow}) {
    return <Button
        variant="outlined" color="default"
        size="small"
        onClick={() => history.push(PATH_ELECTION_REPORT_VIEW(electionId, tallySheetListRow.tallySheetId))}
    >
        View
    </Button>
}

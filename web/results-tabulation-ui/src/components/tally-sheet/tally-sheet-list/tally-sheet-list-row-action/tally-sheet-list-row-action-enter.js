import {PATH_ELECTION_DATA_ENTRY_EDIT} from "../../../../App";
import Button from "@material-ui/core/Button";
import React from "react";

export default function TallySheetListRowActionEnter({history, electionId, tallySheetListRow}) {
    return <Button
        variant="outlined" color="default"
        size="small"
        onClick={() => history.push(PATH_ELECTION_DATA_ENTRY_EDIT(electionId, tallySheetListRow.tallySheetId))}
    >
        Enter
    </Button>
}

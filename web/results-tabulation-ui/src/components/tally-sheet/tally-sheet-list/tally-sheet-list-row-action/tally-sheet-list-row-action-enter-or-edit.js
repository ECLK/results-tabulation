import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../../App";
import Button from "@material-ui/core/Button";
import React from "react";
import {TALLY_SHEET_STATUS_ENUM} from "../../../../services/tabulation-api";

export default function TallySheetListRowActionEnterOrEdit({history, electionId, tallySheetListRow}) {

    let buttonText = "EDIT";
    let disabled = false;
    if (tallySheetListRow.tallySheetStatus === TALLY_SHEET_STATUS_ENUM.ENTERED) {
        buttonText = "EDIT";
    } else if (tallySheetListRow.tallySheetStatus === TALLY_SHEET_STATUS_ENUM.NOT_ENTERED) {
        buttonText = "ENTER";
    } else {
        disabled = true;
    }

    return <Button
        variant="outlined" color="default"
        size="small"
        disabled={disabled}
        onClick={() => history.push(PATH_ELECTION_TALLY_SHEET_VIEW(electionId, tallySheetListRow.tallySheetId))}
    >
        {buttonText}
    </Button>
}

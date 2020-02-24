import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../../App";
import Button from "@material-ui/core/Button";
import React from "react";
import {TALLY_SHEET_STATUS_ENUM} from "../../../../services/tabulation-api";

export default function TallySheetListRowActionVerify({history, electionId, tallySheetListRow}) {
    return <Button
        variant="outlined" color="default"
        disabled={!(tallySheetListRow.tallySheetStatus === TALLY_SHEET_STATUS_ENUM.SUBMITTED)}
        size="small"
        onClick={() => history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetListRow.tallySheetId))}
    >
        Verify
    </Button>
}

import React, {useContext} from "react";
import {
    WORKFLOW_STATUS_TYPE_CERTIFIED,
    WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
    WORKFLOW_STATUS_TYPE_EMPTY,
    WORKFLOW_STATUS_TYPE_NOTIFIED,
    WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
    WORKFLOW_STATUS_TYPE_RELEASED,
    WORKFLOW_STATUS_TYPE_SAVED,
    WORKFLOW_STATUS_TYPE_SUBMITTED,
    WORKFLOW_STATUS_TYPE_VERIFIED
} from "./constants/WORKFLOW_STATUS_TYPE";
import {TallySheetContext} from "../../services/tally-sheet.provider";


const WORKFLOW_STATUS_DESCRIPTION = {
    [WORKFLOW_STATUS_TYPE_SAVED]: "In Progress",
    [WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED]: "Changes Requested",
    [WORKFLOW_STATUS_TYPE_SUBMITTED]: "Submitted",
    [WORKFLOW_STATUS_TYPE_VERIFIED]: "Verified",
    [WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY]: "Ready to Certify.",
    [WORKFLOW_STATUS_TYPE_CERTIFIED]: "Certified",
    [WORKFLOW_STATUS_TYPE_NOTIFIED]: "Release Notified",
    [WORKFLOW_STATUS_TYPE_RELEASED]: "Released"
};

export default function TallySheetStatusDescription(props) {
    const tallySheetContext = useContext(TallySheetContext);

    const {tallySheetId} = props;
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const tallySheetStatus = tallySheet.workflowInstance.status;

    if (tallySheetStatus && WORKFLOW_STATUS_DESCRIPTION[tallySheetStatus]) {
        return <div style={{color: "#5178c8", fontWeight: 900, fontSize: 16, padding: 15}}>
            {WORKFLOW_STATUS_DESCRIPTION[tallySheetStatus]}
        </div>
    } else {
        return null;
    }
}

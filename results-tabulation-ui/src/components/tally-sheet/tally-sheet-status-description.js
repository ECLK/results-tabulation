import React, {useContext} from "react";
import {
    WORKFLOW_STATUS_TYPE_CERTIFIED,
    WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
    WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, WORKFLOW_STATUS_TYPE_RELEASED,
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_SUBMITTED, WORKFLOW_STATUS_TYPE_VERIFIED
} from "./constants/WORKFLOW_STATUS_TYPE";
import {TallySheetContext} from "../../services/tally-sheet.provider";


const WORKFLOW_STATUS_DESCRIPTION = {
    [WORKFLOW_STATUS_TYPE_SAVED]: "Still working in progress.",
    [WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED]: "Changes has been requested.",
    [WORKFLOW_STATUS_TYPE_SUBMITTED]: "Submitted for verification.",
    [WORKFLOW_STATUS_TYPE_VERIFIED]: "This is a verified report.",
    [WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY]: "This report is ready to certify.",
    [WORKFLOW_STATUS_TYPE_CERTIFIED]: "This report has been certified and ready to release.",
    [WORKFLOW_STATUS_TYPE_RELEASED]: "This report has been released.",
};

export default function TallySheetStatusDescription(props) {
    const tallySheetContext = useContext(TallySheetContext);

    const {tallySheetId} = props;
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const tallySheetStatus = tallySheet.workflowInstance.status;

    if (tallySheetStatus && WORKFLOW_STATUS_DESCRIPTION[tallySheetStatus]) {
        return <div className="report-view-status-text">
            {WORKFLOW_STATUS_DESCRIPTION[tallySheetStatus]}
        </div>
    } else {
        return null;
    }
}

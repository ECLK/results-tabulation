import React from "react";
import DataEntryEdit from "./data-entry-edit";
import ReportView from "./report-view";

export default function TallySheetView(props) {
    const {tallySheet} = props;
    const saveAllowed = tallySheet.workflowInstance.actions.filter(action => {
        return action.allowed && action.actionType === "SAVE";
    }).length > 0;

    if (!tallySheet.template.isDerived && saveAllowed) {
        return <DataEntryEdit {...props}/>
    } else {
        return <ReportView {...props}/>
    }
}

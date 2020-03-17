import React, {useContext} from "react";
import DataEntryEdit from "./data-entry-edit";
import ReportView from "./report-view";
import {TallySheetContext} from "../services/tally-sheet.provider";

export default function TallySheetView(props) {
    const {getById} = useContext(TallySheetContext);
    const tallySheet = getById(props.tallySheetId);

    const saveAllowed = tallySheet.workflowInstance.actions.filter(action => {
        return action.allowed && action.actionType === "SAVE";
    }).length > 0;

    if (!tallySheet.template.isDerived && saveAllowed) {
        return <DataEntryEdit {...props}/>
    } else {
        return <ReportView {...props}/>
    }
}

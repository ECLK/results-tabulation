import React, {useContext} from "react";
import DataEntryEdit from "./data-entry-edit";
import ReportView from "./report-view";
import {TallySheetContext} from "../services/tally-sheet.provider";
import {WORKFLOW_ACTION_TYPE_SAVE} from "../components/tally-sheet/constants/WORKFLOW_ACTION_TYPE";

export default function TallySheetView(props) {
    const tallySheetContext = useContext(TallySheetContext);
    const tallySheet = tallySheetContext.getTallySheetById(props.tallySheetId);

    const saveAllowed = tallySheet.workflowInstance.actions.filter(action => {
        return action.allowed && action.actionType === WORKFLOW_ACTION_TYPE_SAVE;
    }).length > 0;

    if (!tallySheet.template.isDerived && saveAllowed) {
        return <DataEntryEdit {...props}/>
    } else {
        return <ReportView {...props}/>
    }
}

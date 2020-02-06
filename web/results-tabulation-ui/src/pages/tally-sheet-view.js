import React from "react";
import DataEntryEdit from "./data-entry-edit";
import ReportView from "./report-view";

export default function TallySheetView(props) {
    const {tallySheet} = props;

    if (!tallySheet.template.isDerived && !tallySheet.submittedVersionId) {
        return <DataEntryEdit {...props}/>
    } else {
        return <ReportView {...props}/>
    }
}

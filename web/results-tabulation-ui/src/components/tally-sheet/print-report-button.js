import React from "react";
import {getTallySheetVersionHtml} from "../../services/tabulation-api";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";

export default function PrintReportButton(props) {
    
    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await getTallySheetVersionHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";

export default function PrintReportButton(props) {
    const {getTallySheetVersionHtml} = useContext(TallySheetContext);

    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await getTallySheetVersionHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

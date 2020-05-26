import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";

export default function PrintReportButton(props) {
    const tallySheetContext = useContext(TallySheetContext);

    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await tallySheetContext.fetchTallySheetVersionHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

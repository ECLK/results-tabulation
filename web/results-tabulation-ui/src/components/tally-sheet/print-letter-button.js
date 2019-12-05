import React from "react";
import {getTallySheetVersionLetterHtml} from "../../services/tabulation-api";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";

export default function PrintLetterButton(props) {


    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await getTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

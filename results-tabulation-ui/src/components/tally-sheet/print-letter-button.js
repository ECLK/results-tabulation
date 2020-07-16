import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";
import {USE_PDF_SERVICE} from "../../config";

export default function PrintLetterButton(props) {
    const tallySheetContext = useContext(TallySheetContext);
    
    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await tallySheetContext.fetchTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId);
    };

    const fetchDataUrl = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await tallySheetContext.fetchTallySheetVersionLetterPdfDataUrl(tallySheetId, tallySheetVersionId);
    };

    const additionalProps = {};
    if (USE_PDF_SERVICE) {
        additionalProps["fetchDataUrl"] = fetchDataUrl;
    } else {
        additionalProps["fetchHtml"] = fetchHtml;
    }

    return <FetchHtmlAndPrintButton
        {...props}
        {...additionalProps}
    />
}

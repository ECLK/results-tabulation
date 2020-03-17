import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";

export default function PrintLetterButton(props) {
    const {getTallySheetVersionLetterHtml} = useContext(TallySheetContext);


    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await getTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

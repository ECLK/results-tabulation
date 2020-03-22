import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";

export default function PrintLetterButton(props) {
    const tallySheetContext = useContext(TallySheetContext);


    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;

        return await tallySheetContext.fetchTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId);
    };

    return <FetchHtmlAndPrintButton
        {...props}
        fetchHtml={fetchHtml}
    />
}

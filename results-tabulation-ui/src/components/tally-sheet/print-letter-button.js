import React, {useContext} from "react";
import FetchHtmlAndPrintButton from "./fetch-html-and-print-button";
import {TallySheetContext} from "../../services/tally-sheet.provider";
import {USE_PDF_SERVICE} from "../../config";
import {DialogContext} from "../../services/dialog.provider";;
import {SignatureSelectionDialog} from "./signature-selection-dialog";

export default function PrintLetterButton(props) {
    const tallySheetContext = useContext(TallySheetContext);
    const dialogContext = useContext(DialogContext);

    const fetchHtml = async () => {
        const {tallySheetId, tallySheetVersionId} = props;
        try {
            let signatures = await dialogContext.push({
                render({open, handleClose, handleOk}) {
                    return <SignatureSelectionDialog open={open} handleClose={handleClose} handleOk={handleOk}/>
                }
            });

            return await tallySheetContext.fetchTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId, signatures);
        } catch (e) {
        }
    };

    const fetchDataUrl = async () => {
        const {tallySheetId, tallySheetVersionId} = props;
        try {
            let signatures = await dialogContext.push({
                render({open, handleClose, handleOk}) {
                    return <SignatureSelectionDialog open={open} handleClose={handleClose} handleOk={handleOk}/>
                }
            });

            return await tallySheetContext.fetchTallySheetVersionLetterPdfDataUrl(tallySheetId, tallySheetVersionId, signatures);
        } catch (e) {
        }
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

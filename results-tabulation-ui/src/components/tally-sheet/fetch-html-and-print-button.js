import React, {useContext, useState} from "react";
import Button from "@material-ui/core/Button";
import {getErrorCode, getErrorMessage} from "../../utils";
import {MESSAGE_TYPES, MessagesContext} from "../../services/messages.provider";
import {TallySheetContext} from "../../services/tally-sheet.provider";

export default function FetchHtmlAndPrintButton(props) {
    const {fetchHtml, onClick, fetchDataUrl} = props;

    const messagesContext = useContext(MessagesContext);

    const {tallySheetId, tallySheetVersionId, children} = props;
    const [printJobsList, setPrintJobsList] = useState([]);
    const [printJobsMap, setPrintJobsMap] = useState({});

    const onHtmlContentIsReady = (printJob) => (event) => {
        printJob.ref.current.contentWindow.print();
    };

    const onPrintClick = () => async (event) => {
        onClick && onClick();

        const printJob = {
            id: null,
            processing: true,
            src: null,
            srcDoc: null,
            onLoad: (event) => {
                onHtmlContentIsReady(printJob)(event)
            },
            ref: React.createRef()
        };

        await setPrintJobsList((printJobs) => {
            printJob.id = printJobs.length;

            return [
                ...printJobs,
                printJob.id
            ]
        });

        await setPrintJobsMap((printJobsMap) => {
            return {...printJobsMap, [printJob.id]: printJob}
        });

        try {
            if (fetchHtml) {
                const srcDoc = await fetchHtml();
                await setPrintJobsMap((printJobsMap) => {
                    return {
                        ...printJobsMap,
                        [printJob.id]: {
                            ...printJob,
                            srcDoc: srcDoc
                        }
                    }
                });
            } else if (fetchDataUrl) {
                const src = await fetchDataUrl();
                await setPrintJobsMap((printJobsMap) => {
                    return {
                        ...printJobsMap,
                        [printJob.id]: {
                            ...printJob,
                            src: src
                        }
                    }
                });
            }
        } catch (e) {
            messagesContext.push({
                messageTitle: "Error",
                messageBody: getErrorMessage(getErrorCode(e)),
                messageType: MESSAGE_TYPES.ERROR
            });
        }
    };

    return <Button
        variant={props.variant}
        color={props.color}
        size={props.size}
        disabled={props.disabled}
        onClick={onPrintClick()}
    >
        {printJobsList.map((printJobId) => {
            const printJob = printJobsMap[printJobId];

            if (printJob && printJob.src) {
                return <iframe
                    key={printJobId}
                    style={{display: 'none'}}
                    src={printJob.src}
                    onLoad={printJob.onLoad}
                    ref={printJob.ref}
                />
            } else if (printJob && printJob.srcDoc) {
                return <iframe
                    key={printJobId}
                    style={{display: 'none'}}
                    srcDoc={printJob.srcDoc}
                    onLoad={printJob.onLoad}
                    ref={printJob.ref}
                />
            } else {
                return null
            }

        })}

        {children}
    </Button>
}

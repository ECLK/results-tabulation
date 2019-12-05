import React, {useState} from "react";
import Button from "@material-ui/core/Button";

export default function FetchHtmlAndPrintButton(props) {
    const {fetchHtml} = props;

    const {tallySheetId, tallySheetVersionId, children} = props;
    const [printJobsList, setPrintJobsList] = useState([]);
    const [printJobsMap, setPrintJobsMap] = useState({});

    const onHtmlContentIsReady = (printJob) => (event) => {
        printJob.ref.current.contentWindow.print();
    };

    const onPrintClick = () => async (event) => {
        const printJob = {
            id: null,
            processing: true,
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

            if (printJob && printJob.srcDoc) {
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

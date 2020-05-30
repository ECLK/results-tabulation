import React, {useContext, useEffect, useState} from "react";
import {
    PATH_ELECTION_TALLY_SHEET_LIST,
    PATH_ELECTION_TALLY_SHEET_VIEW
} from "../App";
import Processing from "../components/processing";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import {TabulationTallySheetPage} from "./index";
import TallySheetActions from "../components/tally-sheet/tally-sheet-actions";
import {TallySheetContext} from "../services/tally-sheet.provider";
import {WORKFLOW_ACTION_TYPE_VIEW} from "../components/tally-sheet/constants/WORKFLOW_ACTION_TYPE";
import TallySheetStatusDescription from "../components/tally-sheet/tally-sheet-status-description";
import Error from "../components/error";

export default function ReportView(props) {
    const tallySheetContext = useContext(TallySheetContext);

    const {history, election, messages} = props;
    const {electionId, rootElection, voteType} = election;
    const tallySheet = tallySheetContext.getTallySheetById(props.tallySheetId);

    const [tallySheetVersionHtml, setTallySheetVersionHtml] = useState(null);
    const [processing, setProcessing] = useState(true);
    const [iframeHeight, setIframeHeight] = useState(600);
    const [iframeWidth] = useState("100%");
    const iframeRef = React.createRef();

    let tallySheetVersionId = props.tallySheetVersionId;
    const {latestVersion} = tallySheet;
    if (!tallySheetVersionId && latestVersion) {
        tallySheetVersionId = latestVersion.tallySheetVersionId;
    }

    const fetchTallySheetVersion = async () => {
        const {tallySheetId} = tallySheet;

        if (tallySheetVersionId) {
            const tallySheetVersionHtml = await tallySheetContext.fetchTallySheetVersionHtml(tallySheetId, tallySheetVersionId);

            setTallySheetVersionHtml(tallySheetVersionHtml)
        }

        setProcessing(false);
    };


    useEffect(() => {
        fetchTallySheetVersion();
    }, []);


    const handleIframeHeight = () => (evt) => {
        setIframeHeight(evt.target.contentDocument.documentElement.scrollHeight + 50);
    };

    const handlePrint = () => (evt) => {
        iframeRef.current.contentWindow.print();
    }

    function getTallySheetListLink() {
        const {tallySheetCode} = tallySheet;

        return PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)
    }


    const getReportViewJsx = () => {
        const {tallySheetCode, tallySheetStatus, area, tallySheetId} = tallySheet;
        const {areaName} = area;
        let tallySheetVersionHtmlJsx = null;

        const additionalBreadCrumbLinks = [
            {
                label: getTallySheetCodeStr({tallySheetCode, voteType}).toLowerCase(),
                to: getTallySheetListLink()
            },
            {
                label: areaName.toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId)
            }
        ];

        if (tallySheetVersionId) {
            tallySheetVersionHtmlJsx = <iframe
                style={{border: "none", width: "100%"}}
                height={iframeHeight}
                width={iframeWidth}
                srcDoc={tallySheetVersionHtml}
                onLoad={handleIframeHeight()}
                ref={iframeRef}
            >
            </iframe>;

            additionalBreadCrumbLinks.push({
                label: tallySheetVersionId,
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId, tallySheetVersionId)
            })
        } else {
            tallySheetVersionHtmlJsx =
                <Error title="Tally sheet is empty" body="There's no content available to preview."/>
        }

        return <TabulationTallySheetPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}
                                         tallySheet={tallySheet} history={history}>
            <div className="page-content">
                <div className="report-view-status">
                    <div className="report-view-status-actions">
                        <TallySheetActions
                            tallySheetId={tallySheetId}
                            electionId={electionId} history={history}
                            filter={(action) => action.actionType !== WORKFLOW_ACTION_TYPE_VIEW}
                        />
                    </div>
                    <TallySheetStatusDescription tallySheetId={tallySheetId}/>
                </div>

                <Processing showProgress={processing}>{tallySheetVersionHtmlJsx}</Processing>
            </div>
        </TabulationTallySheetPage>
    };

    return getReportViewJsx()
}

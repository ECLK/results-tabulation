import React, {useContext, useEffect, useState} from "react";
import {TALLY_SHEET_STATUS_ENUM} from "../services/tabulation-api";
import {
    PATH_ELECTION_TALLY_SHEET_LIST,
    PATH_ELECTION_TALLY_SHEET_VIEW
} from "../App";
import Processing from "../components/processing";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import TabulationPage from "./index";
import TallySheetActions from "../components/tally-sheet/tally-sheet-actions";
import {TallySheetContext} from "../services/tally-sheet.provider";
import {WORKFLOW_ACTION_TYPE_VIEW} from "../components/tally-sheet/constants/WORKFLOW_ACTION_TYPE";

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

        const additionalBreadCrumbLinks = [
            {
                label: getTallySheetCodeStr({tallySheetCode, voteType}).toLowerCase(),
                to: getTallySheetListLink()
            },
            {
                label: areaName.toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId)
            },
            {
                label: tallySheetVersionId,
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId, tallySheetVersionId)
            }
        ];

        return <TabulationPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}>
            <div className="page-content">
                <div>{rootElection.electionName}</div>
                <div>{getTallySheetCodeStr({tallySheetCode, voteType})}</div>


                <div className="report-view-status">
                    <div className="report-view-status-actions">
                        <TallySheetActions
                            tallySheetId={tallySheetId}
                            electionId={electionId} history={history}
                            filter={(action) => action.actionType !== WORKFLOW_ACTION_TYPE_VIEW}
                        />
                    </div>
                    <div className="report-view-status-text">
                        {(() => {
                            if (tallySheetStatus == TALLY_SHEET_STATUS_ENUM.SUBMITTED) {
                                return "This report has been submitted to the system and waiting for verification";
                            } else if (tallySheetStatus == TALLY_SHEET_STATUS_ENUM.VIEWED) {
                                return "This report has been not verified yet";
                            } else if (tallySheetStatus == TALLY_SHEET_STATUS_ENUM.ENTERED) {
                                return "This report has no submitted or verified information. The editing is still in progress.";
                            } else if (tallySheetStatus == TALLY_SHEET_STATUS_ENUM.VERIFIED) {
                                return "This report has been verified.";
                            } else if (tallySheetStatus == TALLY_SHEET_STATUS_ENUM.RELEASED) {
                                return "This report has been released.";
                            }
                        })()}
                    </div>
                </div>

                <Processing showProgress={processing}>
                    <iframe
                        style={{border: "none", width: "100%"}}
                        height={iframeHeight}
                        width={iframeWidth}
                        srcDoc={tallySheetVersionHtml}
                        onLoad={handleIframeHeight()}
                        ref={iframeRef}
                    >
                    </iframe>
                </Processing>
            </div>
        </TabulationPage>
    };

    return getReportViewJsx()
}

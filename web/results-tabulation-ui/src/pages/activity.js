import React, {useContext, useEffect, useState} from "react";
import {TALLY_SHEET_STATUS_ENUM} from "../services/tabulation-api";
import {
    PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW,
    PATH_ELECTION_TALLY_SHEET_LIST,
    PATH_ELECTION_TALLY_SHEET_VIEW
} from "../App";
import Processing from "../components/processing";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import TabulationPage from "./index";
import TallySheetActions from "../components/tally-sheet/tally-sheet-actions";
import {TallySheetContext} from "../services/tally-sheet.provider";
import {WORKFLOW_ACTION_TYPE_VIEW} from "../components/tally-sheet/constants/WORKFLOW_ACTION_TYPE";

export default function ActivityView({tallySheetId, history, election, messages}) {
    const {electionId, rootElection, voteType} = election;

    const tallySheetContext = useContext(TallySheetContext);

    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);
    const [fileMap, setFileMap] = useState({});
    const [tallySheetWorkflowLogList, setTallySheetWorkflowLogList] = useState([]);
    const [processing, setProcessing] = useState(true);


    useEffect(() => {
        fetchTallySheetWorkflowLog();
    }, [tallySheetId]);

    // async function fetchFiles(proof) {
    //     const {scannedFiles} = proof;
    //     for (let i = 0; i < scannedFiles.length; i++) {
    //         const {fileId} = scannedFiles[i];
    //         console.log(`======= ${proof.proofId} - ${fileId}`);
    //         const file = await tallySheetContext.getTallySheetProofFileDataUrl(tallySheetId, fileId);
    //         setFileMap(prevState => {
    //             return {...prevState, [fileId]: file};
    //         });
    //     }
    // }

    async function fetchTallySheetWorkflowLog() {
        setProcessing(true);
        const _tallySheetWorkflowLogList = await tallySheetContext.getTallySheetWorkflowLogList(tallySheetId);
        setTallySheetWorkflowLogList(_tallySheetWorkflowLogList);
        setProcessing(false);
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
                label: "activity",
                to: PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW(tallySheetId)
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
                    <div>
                        <ul>
                            {tallySheetWorkflowLogList.map(tallySheetWorkflowLog => {
                                const {workflowInstanceLogId, proof, action, createdBy, createdAt, metaDataMap} = tallySheetWorkflowLog;
                                const {actionName, actionType} = action;
                                const {tallySheetVersionId} = metaDataMap;
                                return <li key={workflowInstanceLogId}>
                                    [{actionType}] <strong>{actionName}</strong> ({createdBy} @ {createdAt})
                                    <a onClick={() => {
                                        history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId, tallySheetVersionId))
                                    }}>
                                        {tallySheetVersionId}
                                    </a>
                                    <ul>
                                        {proof.scannedFiles.map(({fileId, fileName}) => {
                                            return <li>
                                                <a key={fileId}
                                                   href={"asdasd"}>{fileName}</a> ({createdBy} @ {createdAt})
                                            </li>
                                        })}
                                    </ul>
                                </li>
                            })}
                        </ul>
                    </div>
                </Processing>
            </div>
        </TabulationPage>
    };

    return getReportViewJsx()


}

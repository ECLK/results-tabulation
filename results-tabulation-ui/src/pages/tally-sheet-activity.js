import React, {useContext, useEffect, useState} from "react";
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
import PreviewTallySheetProofFileButton from "../components/tally-sheet/tally-sheet-proof-file-preview-button";
import {Link} from 'react-router-dom';
import {Check, MoveToInbox, Publish, Save, TurnedIn, VerifiedUser, Visibility} from '@material-ui/icons';
import TallySheetStatusDescription from "../components/tally-sheet/tally-sheet-status-description";
import {
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_CE_RO_PR_1
} from "../components/election/extended-election/ParliamentElection2020/TALLY_SHEET_CODE";

export default function TallySheetActivityView({tallySheetId, history, election}) {
    const {electionId, rootElection, voteType} = election;

    const tallySheetContext = useContext(TallySheetContext);

    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);
    const [tallySheetWorkflowLogList, setTallySheetWorkflowLogList] = useState([]);
    const [processing, setProcessing] = useState(true);


    useEffect(() => {
        fetchTallySheetWorkflowLog();
    }, [tallySheetId]);

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

    function ActionIcon(props) {
        if (props.actionType === 'VIEW') {
            return <Visibility className="activity-icon"/>;
        } else if (props.actionType === 'VERIFY') {
            return <Check className="activity-icon"/>;
        } else if (props.actionType === 'SUBMIT') {
            return <TurnedIn className="activity-icon"/>;
        } else if (props.actionType === 'MOVE_TO_CERTIFY') {
            return <MoveToInbox className="activity-icon"/>;
        } else if (props.actionType === 'UPLOAD_PROOF_DOCUMENT') {
            return <Publish className="activity-icon"/>;
        } else if (props.actionType === 'CERTIFY') {
            return <VerifiedUser className="activity-icon"/>;
        } else {
            return <Save className="activity-icon"/>;
        }
    }


    const getReportViewJsx = () => {
        const {tallySheetCode, tallySheetStatus, area, tallySheetId, metaDataMap} = tallySheet;
        const {areaName} = area;
        let additionalBreadCrumbLinks = [];

        if (metaDataMap["partyId"]) {
            const partyId = metaDataMap["partyId"];
            const party = election.partyMap[partyId];

            if ([TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22, TALLY_SHEET_CODE_PE_CE_RO_PR_1].indexOf(tallySheetCode) >= 0) {
                additionalBreadCrumbLinks = [{
                    label: getTallySheetCodeStr({tallySheetCode, voteType}) + " - " + party.partyName.toLowerCase(),
                    to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType, partyId)
                }, {
                    label: tallySheet.area.areaName.toLowerCase(),
                    to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
                }];
            } else {
                additionalBreadCrumbLinks = [{
                    label: getTallySheetCodeStr({tallySheetCode, voteType}),
                    to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType)
                }, {
                    label: (party.partyName + " - " + tallySheet.area.areaName).toLowerCase(),
                    to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
                }];
            }
        } else {
            additionalBreadCrumbLinks = [{
                label: getTallySheetCodeStr({tallySheetCode, voteType}),
                to: PATH_ELECTION_TALLY_SHEET_LIST(election.electionId, tallySheetCode, voteType)
            }, {
                label: tallySheet.area.areaName.toLowerCase(),
                to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId)
            }];
        }

        return <TabulationPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}>
            <div className="page-content">
                <div>{rootElection.electionName}</div>
                <div>{getTallySheetCodeStr({tallySheetCode, voteType})}</div>

                <Processing showProgress={processing}>
                    <div className="activity-wrapper">
                        <ul className="activity-list">
                            {tallySheetWorkflowLogList.map(tallySheetWorkflowLog => {
                                const {workflowInstanceLogId, proof, action, createdBy, createdAt, metaDataMap} = tallySheetWorkflowLog;
                                const {actionName, actionType} = action;
                                const {tallySheetVersionId} = metaDataMap;
                                return <li key={workflowInstanceLogId} className="activity-row">
                                    <div className="activity-block"><ActionIcon actionType={actionType}/></div>
                                    <div className="activity-block activity-details">
                                        <strong>{actionName}</strong> by {createdBy} @ {createdAt}&nbsp;
                                        <Link className="activity-tallysheet-link"
                                              to={
                                                  PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId, tallySheetVersionId)
                                              }
                                              style={{
                                                  color: "#5079c8",
                                                  textDecoration: "underline"
                                              }}
                                        >
                                            {tallySheetVersionId}
                                        </Link>
                                        <ul>
                                            {proof.scannedFiles.map(({fileId, fileName}) => {
                                                return <li className="activity-proof">
                                                    <PreviewTallySheetProofFileButton
                                                        tallySheetId={tallySheetId} fileId={fileId}
                                                        className="activity-proof-link"
                                                        style={{
                                                            color: "#5079c8",
                                                            textDecoration: "underline"
                                                        }}
                                                    >
                                                        {fileName}
                                                    </PreviewTallySheetProofFileButton> ({createdBy} @ {createdAt})
                                                </li>
                                            })}
                                        </ul>
                                    </div>
                                </li>
                            })}
                        </ul>
                    </div>
                </Processing>
            </div>
        </TabulationPage>
    };

    return getReportViewJsx();
}

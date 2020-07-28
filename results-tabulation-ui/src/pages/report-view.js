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
import Button from "@material-ui/core/Button";
import {
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_CE_RO_PR_1
} from "../components/election/extended-election/ParliamentElection2020/TALLY_SHEET_CODE";

export default function ReportView(props) {
    const tallySheetContext = useContext(TallySheetContext);

    const {history, election} = props;
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
        const {tallySheetCode, metaDataMap, area, tallySheetId, election} = tallySheet;
        const {areaName} = area;
        let tallySheetVersionHtmlJsx;
        let additionalBreadCrumbLinks;

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

        if (tallySheetVersionId) {
            tallySheetVersionHtmlJsx = <iframe
                style={{border: "none", width: "100%", padding: 5, boxSizing: "border-box"}}
                height={iframeHeight}
                width={iframeWidth}
                srcDoc={tallySheetVersionHtml}
                onLoad={handleIframeHeight()}
                ref={iframeRef}
            >
            </iframe>;

            // additionalBreadCrumbLinks.push({
            //     label: tallySheetVersionId,
            //     to: PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId, tallySheetVersionId)
            // })
        } else {
            tallySheetVersionHtmlJsx =
                <Error title="Tally sheet is empty" body="There's no content available to preview."/>
        }

        return <TabulationTallySheetPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}
                                         tallySheet={tallySheet} history={history}>
            <div className="page-content">
                <div className="report-view-status"
                     style={{display: "flex", marginBottom: 10, borderBottom: "2px dashed #9E9E9E"}}>

                    <div><TallySheetStatusDescription tallySheetId={tallySheetId}/></div>

                    <div style={{flex: 1}}>
                        {(() => {
                            if (tallySheetVersionId && tallySheetVersionId !== latestVersion.tallySheetVersionId) {
                                return <div style={{padding: 10, textAlign: "right"}}>
                                    This document is
                                    <strong>&nbsp;OUTDATED.&nbsp;</strong> Click&nbsp;
                                    <Button variant="contained" size="small" color="secondary"
                                            onClick={() => history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheetId))}>
                                        Here
                                    </Button>
                                    &nbsp;to see the latest changes.
                                </div>
                            } else {
                                return <div className="report-view-status-actions">
                                    <TallySheetActions
                                        tallySheetId={tallySheetId}
                                        electionId={electionId} history={history}
                                        filter={(action) => action.actionType !== WORKFLOW_ACTION_TYPE_VIEW}
                                    />
                                </div>
                            }
                        })()}
                    </div>

                </div>

                <Processing showProgress={processing}>{tallySheetVersionHtmlJsx}</Processing>
            </div>
        </TabulationTallySheetPage>
    };

    return getReportViewJsx()
}

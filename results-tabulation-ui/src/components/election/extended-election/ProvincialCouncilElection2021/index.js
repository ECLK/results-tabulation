import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_BY_ID,
    PATH_ELECTION_TALLY_SHEET_LIST
} from "../../../../App";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PCE_31,
    TALLY_SHEET_CODE_PCE_34,
    TALLY_SHEET_CODE_PCE_35,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_1,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_2,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_3,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_4,
    TALLY_SHEET_CODE_PCE_CE_RO_V1,
    TALLY_SHEET_CODE_PCE_R1,
    TALLY_SHEET_CODE_PCE_R1_PV,
    TALLY_SHEET_CODE_PCE_CE_RO_V2,
    TALLY_SHEET_CODE_PCE_R2,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_1,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_2,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_3,
    TALLY_SHEET_CODE_PCE_42,
    TALLY_SHEET_CODE_PCE_PD_V,
    TALLY_SHEET_CODE_PCE_PC_V,
    TALLY_SHEET_CODE_PCE_PC_CD,
    TALLY_SHEET_CODE_PCE_PC_BS_1,
    TALLY_SHEET_CODE_PCE_PC_BS_2,
    TALLY_SHEET_CODE_PCE_PC_SA_1,
    TALLY_SHEET_CODE_PCE_PC_SA_2
} from "./TALLY_SHEET_CODE";
import {Link, useHistory} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import Button from "@material-ui/core/Button";
import React, {useContext, useEffect, useState} from "react";
import * as Settings from './settings'
import ExtendedElectionDefault from "../extended-election-default";
import ProvincialCouncilElection2021TallySheetEdit from "./tally-sheet-edit";
import {ElectionContext} from "../../../../services/election.provider";
import Processing from "../../../processing";
import {VOTE_TYPE_NON_POSTAL, VOTE_TYPE_POSTAL, VOTE_TYPE_POSTAL_AND_NON_POSTAL} from "../../constants/VOTE_TYPE";
import {DialogContext} from "../../../../services/dialog.provider";
import {MessagesContext} from "../../../../services/messages.provider";
import {TallySheetProofFilePreviewDialog} from "../../../tally-sheet/tally-sheet-proof-file-preview-dialog";
import {PartySelectionDialog} from "../../../tally-sheet/party-selection-dialog";

export default class ExtendedElectionProvincialCouncilElection2021 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, ProvincialCouncilElection2021TallySheetEdit);
    }

    getElectionHome() {
        function addDistrictElections(districtElections) {
            let currentDistrictElections = DistrictElections === null ? [] : DistrictElections;

            if (districtElections !== null && districtElections.length > 0) {
                const parentElectionId = districtElections[0].parentElectionId;
                currentDistrictElections["provincial_" + parentElectionId] = districtElections;
            }
            setDistrictElections(currentDistrictElections);

        }

        function setSubElections(provinceElections) {
            setProvinceElections(provinceElections);
            {
                provinceElections !== null && provinceElections.map((districtElection) => {
                    electionContext.getSubElections(districtElection.electionId, null).then(addDistrictElections)
                })
            }
        }

        const history = useHistory();
        const dialogContext = useContext(DialogContext);
        const electionContext = useContext(ElectionContext);
        const [ProvinceElections, setProvinceElections] = useState(null);
        const [DistrictElections, setDistrictElections] = useState(null);

        const {electionId, electionName, rootElectionId, parentElectionId} = this.election;

        const selectPartyAndThen = (then) => () => {
            dialogContext.push({
                render({open, handleClose, handleOk}) {
                    return <PartySelectionDialog
                        electionId={electionId} open={open} handleClose={handleClose}
                        handleOk={handleOk}
                    />
                }
            }).then((party) => party && then(party));
        };

        useEffect(() => {
            if (electionId===rootElectionId || rootElectionId==parentElectionId) {
                electionContext.getSubElections(rootElectionId, null).then(setSubElections)
            }else{
                electionContext.getSubElections(electionId, null).then(setSubElections)
            }
        }, [electionId]);

        if (electionId === rootElectionId || rootElectionId==parentElectionId) {
            return <div className="page-content">
                <h1>{electionName}</h1>
                <Grid container spacing={3}>
                    <Grid item xs={6} className="election-grid">
                        <Grid item xs={12}><h2>Provincial Elections</h2></Grid>
                        <Processing showProgress={ProvinceElections === null}>
                            <div className="election-list">
                                {ProvinceElections !== null && ProvinceElections.map((election) => {
                                    return <div key={election.electionId}>
                                        {election.electionName}<br/>
                                        {DistrictElections !== null && DistrictElections["provincial_" + election.electionId].map((districtElection) => {
                                            return <Link
                                                key={districtElection.electionId}
                                                to={PATH_ELECTION_BY_ID(districtElection.electionId)}
                                                className="election-list-item"
                                            >
                                                {districtElection.electionName}
                                            </Link>
                                        })}
                                    </div>
                                })}
                            </div>
                        </Processing>
                    </Grid>
                    <Grid item xs={6} className="election-grid">
                        <Grid item xs={12}><h2>Provincial Reports</h2></Grid>


                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                {(() => {
                                    let tallySheetCodes = [TALLY_SHEET_CODE_PCE_PC_V,
                                        TALLY_SHEET_CODE_PCE_PC_BS_1,
                                        TALLY_SHEET_CODE_PCE_PC_BS_2,
                                        TALLY_SHEET_CODE_PCE_PC_CD,
                                        TALLY_SHEET_CODE_PCE_PC_SA_1,
                                        TALLY_SHEET_CODE_PCE_PC_SA_2];
                                    let tallySheetCodeLabels = [
                                        "Provincial Vote Results",
                                        "Bonus Seat Allocation 1",
                                        "Bonus Seat Allocation 2",
                                        "Candidates List",
                                        "Seat Allocation 1",
                                        "Seat Allocation 2",
                                    ];

                                    return tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                        return <li key={tallySheetCodeIndex}>
                                            {tallySheetCodeLabels[tallySheetCodeIndex]}
                                            <Link
                                                className="tally-sheet-code-list-item btn-list"
                                                to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                            >
                                                List
                                            </Link>
                                        </li>
                                    });
                                })()}

                            </ul>
                        </Grid>

                    </Grid>
                </Grid>
            </div>
        } else {
            return <div className="page-content">
                <h1>{electionName}</h1>
                <Grid container spacing={3}>
                    <Grid item xs={6} className="election-grid">

                        <Grid item xs={12}><h2>Data Entry</h2></Grid>

                        <Processing showProgress={!ProvinceElections}>
                            {ProvinceElections !== null && ProvinceElections.map(({voteType}) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === VOTE_TYPE_NON_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PCE_35];
                                    tallySheetCodeLabels = ["CE 201", "PCE-35"];
                                } else if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PCE_35];
                                    tallySheetCodeLabels = [`CE 201 PV (${voteType})`, `PCE-35 PV (${voteType})`];
                                } else {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PCE_35];
                                    tallySheetCodeLabels = [`CE 201 (${voteType})`, `PCE-35 (${voteType})`];
                                }

                                return <Grid item xs={12} key={voteType}>
                                    <Grid item xs={12}>
                                        <ul className="tally-sheet-code-list">
                                            {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                                return <li key={tallySheetCodeIndex}>
                                                    {tallySheetCodeLabels[tallySheetCodeIndex]}
                                                    <Link
                                                        className="tally-sheet-code-list-item btn-list"
                                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                                    >
                                                        List
                                                    </Link>

                                                </li>
                                            })}
                                        </ul>
                                    </Grid>
                                </Grid>
                            })}
                        </Processing>

                        <br/>
                        <Divider/>

                        <Grid item xs={12}>
                            <small>Preferences</small>
                        </Grid>


                        <Processing showProgress={!ProvinceElections}>
                            {ProvinceElections !== null && ProvinceElections.map(({voteType}) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === VOTE_TYPE_NON_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_CO_PR_4];
                                    tallySheetCodeLabels = ["PCE-CE-RO-PR-4"];
                                } else if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_CO_PR_4];
                                    tallySheetCodeLabels = [`PCE-CE-RO-PR-4 PV (${voteType})`];
                                } else {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_CO_PR_4];
                                    tallySheetCodeLabels = [`PCE-CE-RO-PR-4 (${voteType})`];
                                }
                                return <Grid item xs={12} key={voteType}>
                                    <Grid item xs={12}>
                                        <ul className="tally-sheet-code-list">
                                            {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                                return <li key={tallySheetCodeIndex}>
                                                    {tallySheetCodeLabels[tallySheetCodeIndex]}
                                                    <a className="tally-sheet-code-list-item btn-list"
                                                       onClick={selectPartyAndThen(({partyId}) => {
                                                           history.push(PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType, partyId))
                                                       })}
                                                    >
                                                        List
                                                    </a>
                                                </li>
                                            })}
                                        </ul>
                                    </Grid>
                                </Grid>
                            })}
                        </Processing>

                    </Grid>
                    <Grid item xs={6} className="election-grid">
                        <Grid item xs={12}><h2>Reports</h2></Grid>

                        <Grid item xs={12}>

                            <Processing showProgress={!ProvinceElections}>
                                {ProvinceElections !== null && ProvinceElections.map(({voteType}) => {
                                    let tallySheetCodes = [];
                                    let tallySheetCodeLabels = [];
                                    if (voteType === VOTE_TYPE_NON_POSTAL) {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_RO_V1, TALLY_SHEET_CODE_PCE_PD_V];
                                        tallySheetCodeLabels = ["PCE-CE-RO-V1", "Polling Division Results"];
                                    } else {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_RO_V1, TALLY_SHEET_CODE_PCE_PD_V];
                                        tallySheetCodeLabels = [`PCE-CE-RO-V1 (${voteType})`, `Polling Division Results (${voteType})`];
                                    }

                                    return <ul className="tally-sheet-code-list" key={voteType}>
                                        {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                            return <li
                                                key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                                <Link
                                                    className="tally-sheet-code-list-item btn-list"
                                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                                >
                                                    List
                                                </Link>
                                            </li>
                                        })}
                                    </ul>
                                })}
                            </Processing>


                            <ul className="tally-sheet-code-list">
                                <li>PCE-CE-RO-V2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PCE_CE_RO_V2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>

                                <li>PCE-R2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PCE_R2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
                            </ul>
                        </Grid>

                        <br/>
                        <Divider/>

                        <Grid item xs={12}>
                            <small>Preferences</small>
                        </Grid>

                        <Grid item xs={12}>
                            <Processing showProgress={!ProvinceElections}>
                                {ProvinceElections !== null && ProvinceElections.map(({voteType}) => {
                                    let tallySheetCodes = [];
                                    let tallySheetCodeLabels = [];
                                    if (voteType === VOTE_TYPE_NON_POSTAL) {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_RO_PR_1];
                                        tallySheetCodeLabels = ["PCE-CE-RO-PR-1 "];
                                    } else {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PCE_CE_RO_PR_1];
                                        tallySheetCodeLabels = [`PCE-CE-RO-PR-1  (${voteType})`];
                                    }

                                    return <ul className="tally-sheet-code-list" key={voteType}>
                                        {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                            return <li
                                                key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                                <a className="tally-sheet-code-list-item btn-list"
                                                   onClick={selectPartyAndThen(({partyId}) => {
                                                       history.push(PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType, partyId))
                                                   })}
                                                >
                                                    List
                                                </a>
                                            </li>
                                        })}
                                    </ul>

                                })}
                            </Processing>
                            <ul className="tally-sheet-code-list">
                                <li>PCE-CE-RO-PR-2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PCE_CE_RO_PR_2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>

                                <li>PCE-CE-RO-PR-3
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PCE_CE_RO_PR_3, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
                            </ul>
                        </Grid>

                        <br/>
                        <Divider/>
                        <Grid item xs={12}>
                            <small>Votes + Preferences</small>
                        </Grid>

                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                <li>PCE-42
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PCE_42, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
                            </ul>
                        </Grid>

                    </Grid>
                </Grid>
            </div>
        }
    }
}

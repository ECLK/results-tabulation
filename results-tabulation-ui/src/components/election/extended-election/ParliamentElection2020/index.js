import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_BY_ID,
    PATH_ELECTION_TALLY_SHEET_LIST
} from "../../../../App";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PE_27,
    TALLY_SHEET_CODE_PE_4,
    TALLY_SHEET_CODE_PE_CE_RO_PR_1,
    TALLY_SHEET_CODE_PE_CE_RO_PR_2,
    TALLY_SHEET_CODE_PE_CE_RO_PR_3,
    TALLY_SHEET_CODE_PE_CE_RO_V1,
    TALLY_SHEET_CODE_PE_CE_RO_V2,
    TALLY_SHEET_CODE_PE_R2,
    TALLY_SHEET_CODE_PE_39,
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_PE_21,
    TALLY_SHEET_CODE_POLLING_DIVISION_RESULTS,
    TALLY_SHEET_CODE_ALL_ISLAND_RESULT
} from "./TALLY_SHEET_CODE";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React, {useContext, useEffect, useState} from "react";
import * as Settings from './settings'
import ExtendedElectionDefault from "../extended-election-default";
import ParliamentElection2020TallySheetEdit from "./tally-sheet-edit";
import {ElectionContext} from "../../../../services/election.provider";
import Processing from "../../../processing";
import {VOTE_TYPE_NON_POSTAL, VOTE_TYPE_POSTAL, VOTE_TYPE_POSTAL_AND_NON_POSTAL} from "../../constants/VOTE_TYPE";

export default class ExtendedElectionParliamentElection2020 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, ParliamentElection2020TallySheetEdit);
    }

    getElectionHome() {
        const electionContext = useContext(ElectionContext);
        const [subElections, setSubElections] = useState(null);

        const {electionId, electionName, rootElectionId} = this.election;
        const voteTypes = [VOTE_TYPE_POSTAL, VOTE_TYPE_NON_POSTAL];

        useEffect(() => {
            electionContext.getSubElections(electionId, null).then(setSubElections);
        }, [electionId]);

        if (electionId === rootElectionId) {
            return <div className="page-content">
                <h1>{electionName}</h1>
                <Grid container spacing={3}>
                    <Grid item xs={9} className="election-grid">
                        <Grid item xs={12}><h2>District Elections</h2></Grid>
                        <Processing showProgress={subElections === null}>
                            <div className="election-list">
                                {subElections !== null && subElections.map((election) => {
                                    const {electionId, electionName} = election;

                                    return <Link
                                        key={electionId} to={PATH_ELECTION_BY_ID(electionId)}
                                        className="election-list-item"
                                    >
                                        {electionName}
                                    </Link>
                                })}
                            </div>
                        </Processing>
                    </Grid>
                    <Grid item xs={3} className="election-grid">
                        <Grid item xs={12}><h2>National Reports</h2></Grid>

                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                <li>All Island Result
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_ALL_ISLAND_RESULT, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
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

                        <Processing showProgress={!subElections}>
                            {subElections !== null && subElections.map(({voteType}) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === VOTE_TYPE_NON_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_39];
                                    tallySheetCodeLabels = ["CE 201", "PE-27", "PE-39"];
                                } else if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_39];
                                    tallySheetCodeLabels = [`CE 201 PV (${voteType})`, `PE-27 PV (${voteType})`, `PE-39 PV (${voteType})`];
                                } else {
                                    tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_39];
                                    tallySheetCodeLabels = [`CE 201 (${voteType})`, `PE-27 (${voteType})`, `PE-39 (${voteType})`];
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

                        <Grid item xs={12}><small>Preferences</small></Grid>


                        <Processing showProgress={!subElections}>
                            {subElections !== null && subElections.map(({voteType}) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === VOTE_TYPE_NON_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22];
                                    tallySheetCodeLabels = ["PE-4", "PE-22"];
                                } else if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22];
                                    tallySheetCodeLabels = [`PE-4 PV (${voteType})`, `PE-22 (${voteType})`];
                                } else {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22];
                                    tallySheetCodeLabels = [`PE-4 (${voteType})`, `PE-22 (${voteType})`];
                                }
                                return <Grid item xs={12} key={voteType}>
                                    <Grid item xs={12}>
                                        <ul className="tally-sheet-code-list">
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
                                    </Grid>
                                </Grid>
                            })}
                        </Processing>

                    </Grid>
                    <Grid item xs={6} className="election-grid">
                        <Grid item xs={12}><h2>Reports</h2></Grid>

                        <Grid item xs={12}>

                            <Processing showProgress={!subElections}>
                                {subElections !== null && subElections.map(({voteType}) => {
                                    let tallySheetCodes = [];
                                    let tallySheetCodeLabels = [];
                                    if (voteType === VOTE_TYPE_NON_POSTAL) {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_V1, TALLY_SHEET_CODE_POLLING_DIVISION_RESULTS];
                                        tallySheetCodeLabels = ["PE-CE-RO-V1", "Polling Division Results"];
                                    } else {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_V1, TALLY_SHEET_CODE_POLLING_DIVISION_RESULTS];
                                        tallySheetCodeLabels = [`PE-CE-RO-V1 (${voteType})`, `Polling Division Results (${voteType})`];
                                    }

                                    return <ul className="tally-sheet-code-list">
                                        {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                            return <li key={voteType}>{tallySheetCodeLabels[tallySheetCodeIndex]}
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
                                <li>PE-CE-RO-V2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_V2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>

                                <li>PE-R2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_R2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
                            </ul>
                        </Grid>

                        <br/>
                        <Divider/>

                        <Grid item xs={12}><small>Preferences</small></Grid>

                        <Grid item xs={12}>
                            <Processing showProgress={!subElections}>
                                {subElections !== null && subElections.map(({voteType}) => {
                                    let tallySheetCodes = [];
                                    let tallySheetCodeLabels = [];
                                    if (voteType === VOTE_TYPE_NON_POSTAL) {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_PR_1];
                                        tallySheetCodeLabels = ["PE-CE-RO-PR-1 "];
                                    } else {
                                        tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_PR_1];
                                        tallySheetCodeLabels = [`PE-CE-RO-PR-1  (${voteType})`];
                                    }

                                    return <ul className="tally-sheet-code-list">
                                        {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                            return <li key={voteType}>{tallySheetCodeLabels[tallySheetCodeIndex]}
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
                                <li>PE-CE-RO-PR-2
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_2, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>

                                <li>PE-CE-RO-PR-3
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_3, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
                                    >
                                        List
                                    </Link>
                                </li>
                            </ul>
                        </Grid>

                        <br/>
                        <Divider/>
                        <Grid item xs={12}><small>Votes + Preferences</small></Grid>

                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                <li>PE-21
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_21, VOTE_TYPE_POSTAL_AND_NON_POSTAL)}
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

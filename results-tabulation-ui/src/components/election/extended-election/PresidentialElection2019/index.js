import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_TALLY_SHEET_LIST
} from "../../../../App";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD, TALLY_SHEET_CODE_PRE_34_AI,
    TALLY_SHEET_CODE_PRE_34_CO, TALLY_SHEET_CODE_PRE_34_ED, TALLY_SHEET_CODE_PRE_34_I_RO, TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_41,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
} from "./TALLY_SHEET_CODE";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React from "react";
import * as Settings from './settings'
import ExtendedElectionDefault from "../extended-election-default";
import PresidentialElection2019TallySheetEdit from "./tally-sheet-edit";
import {VOTE_TYPE_NON_POSTAL, VOTE_TYPE_POSTAL} from "../../constants/VOTE_TYPE";

export default class ExtendedElectionPresidentialElection2019 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, PresidentialElection2019TallySheetEdit);
    }

    getElectionHome() {
        const {electionId, electionName} = this.election;
        const voteTypes = [VOTE_TYPE_POSTAL, VOTE_TYPE_NON_POSTAL];

        return <div className="page-content">
            <h1>{electionName}</h1>
            <Grid container spacing={3}>
                <Grid item xs={6} className="election-grid">

                    <Grid item xs={12}><h2>Data Entry</h2></Grid>


                    {voteTypes.map((voteType) => {
                        let tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PRE_41];
                        let tallySheetCodeLabels = ["CE 201", "PRE-41"];
                        if (voteType === VOTE_TYPE_POSTAL) {
                            tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PRE_41];
                            tallySheetCodeLabels = ["CE 201 PV (Postal)", "PRE-41 PV (Postal)"];
                        }
                        return <Grid item xs={12} key={voteType}>
                            <Grid item xs={12}>
                                <ul className="tally-sheet-code-list">
                                    {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                        return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
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

                    <br/>
                    <Divider/>

                    <Grid item xs={12}><small>Preferences</small></Grid>

                    {voteTypes.map((voteType) => {
                        let tallySheetCodes = [TALLY_SHEET_CODE_PRE_34_CO];
                        let tallySheetCodeLabels = ["PRE 34 CO"];
                        if (voteType === VOTE_TYPE_POSTAL) {
                            tallySheetCodes = [TALLY_SHEET_CODE_PRE_34_CO];
                            tallySheetCodeLabels = ["PRE 34 CO PV (Postal)"];
                        }
                        return <Grid item xs={12} key={voteType}>
                            <Grid item xs={12}>
                                <ul className="tally-sheet-code-list">
                                    {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                        return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
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
                </Grid>
                <Grid item xs={6} className="election-grid">
                    <Grid item xs={12}><h2>Reports</h2></Grid>

                    <Grid item xs={12}>
                        <ul className="tally-sheet-code-list">
                            {voteTypes.map((voteType) => {
                                let tallySheetCode = TALLY_SHEET_CODE_PRE_30_PD;
                                let tallySheetCodeLabel = "PRE 30 PD";
                                if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodeLabel = "PRE 30 PV (Postal)";
                                }

                                return <li key={voteType}>{tallySheetCodeLabel}
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                    >
                                        List
                                    </Link>
                                </li>
                            })}
                            <li>PRE 30 ED
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PRE_30_ED)}
                                >
                                    List
                                </Link>
                            </li>


                            <li>All Island ED
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS)}
                                >
                                    List
                                </Link>
                            </li>
                            <li>All Island
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS)}
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
                        <ul className="tally-sheet-code-list">
                            {voteTypes.map((voteType) => {
                                let tallySheetCode = TALLY_SHEET_CODE_PRE_34_I_RO;
                                let tallySheetCodeLabel = "PRE 34 I RO";
                                if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodeLabel = "PRE 34 I RO PV (Postal)";
                                }

                                return <li key={voteType}>{tallySheetCodeLabel}
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

                    <br/>
                    <Divider/>

                    <Grid item xs={12}><small>With Preferences</small></Grid>

                    <Grid item xs={12}>
                        <ul className="tally-sheet-code-list">
                            {voteTypes.map((voteType) => {
                                let tallySheetCode = TALLY_SHEET_CODE_PRE_34_PD;
                                let tallySheetCodeLabel = "Revised 30 PD";
                                if (voteType === VOTE_TYPE_POSTAL) {
                                    tallySheetCodeLabel = "Revised 30 PV (Postal)";
                                }

                                return <li key={voteType}>{tallySheetCodeLabel}
                                    <Link
                                        className="tally-sheet-code-list-item btn-list"
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                    >
                                        List
                                    </Link>
                                </li>
                            })}
                            <li>Revised 30 ED
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PRE_34_ED)}
                                >
                                    List
                                </Link>
                            </li>
                            <li>Revised All Island
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PRE_34_AI)}
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

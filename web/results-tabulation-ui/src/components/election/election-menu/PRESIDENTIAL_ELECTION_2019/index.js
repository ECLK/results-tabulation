import BreadCrumb from "../../../bread-crumb";
import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_DATA_ENTRY,
    PATH_ELECTION_REPORT, PATH_ELECTION_RESULTS_RELEASE,
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD, TALLY_SHEET_CODE_PRE_34_AI,
    TALLY_SHEET_CODE_PRE_34_CO, TALLY_SHEET_CODE_PRE_34_ED, TALLY_SHEET_CODE_PRE_34_I_RO, TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_41,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
} from "../../../../App";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React from "react";

export default function PRESIDENTIAL_ELECTION_2019(
    {
        election
    }
) {
    const {electionId, electionName, subElections} = election;

    return <div className="page-content">
        <h1>{electionName}</h1>

        <Grid container spacing={3}>
            <Grid item xs={4} className="election-grid">

                <Grid item xs={12}><h2>Data Entry</h2></Grid>


                {subElections.map((subElection) => {
                    const subElectionId = subElection.electionId;
                    let subElectionSuffix = "";
                    let tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PRE_41];
                    let tallySheetCodeLabels = ["CE 201", "PRE-41"];
                    if (subElection.voteType === "Postal") {
                        tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PRE_41];
                        tallySheetCodeLabels = ["CE 201 PV (Postal)", "PRE-41 PV (Postal)"];
                    }
                    return <Grid item xs={12} key={subElectionId}>
                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId)}
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

                {subElections.map((subElection) => {
                    const subElectionId = subElection.electionId;
                    let tallySheetCodes = [TALLY_SHEET_CODE_PRE_34_CO];
                    let tallySheetCodeLabels = ["PRE 34 CO"];
                    if (subElection.voteType === "Postal") {
                        tallySheetCodes = [TALLY_SHEET_CODE_PRE_34_CO];
                        tallySheetCodeLabels = ["PRE 34 CO PV (Postal)"];
                    }
                    return <Grid item xs={12} key={subElectionId}>
                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId)}
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
            <Grid item xs={4} className="election-grid">
                <Grid item xs={12}><h2>Reports</h2></Grid>

                <Grid item xs={12}>
                    <ul className="tally-sheet-code-list">
                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PRE_30_PD;
                            let tallySheetCodeLabel = "PRE 30 PD";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PRE 30 PV (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(electionId, tallySheetCode, subElectionId)}
                                >
                                    List
                                </Link>
                            </li>
                        })}
                        <li>PRE 30 ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_30_ED)}
                            >
                                List
                            </Link>
                        </li>


                        <li>All Island ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS)}
                            >
                                List
                            </Link>
                        </li>
                        <li>All Island
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS)}
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
                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PRE_34_I_RO;
                            let tallySheetCodeLabel = "PRE 34 I RO";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PRE 34 I RO PV (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(electionId, tallySheetCode, subElectionId)}
                                >
                                    List
                                </Link>
                            </li>
                        })}


                        {/*<li>PRE 34*/}
                        {/*<Link*/}
                        {/*disabled={true}*/}
                        {/*className="tally-sheet-code-list-item btn-list"*/}
                        {/*to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_34)}*/}
                        {/*>*/}
                        {/*List*/}
                        {/*</Link>*/}
                        {/*</li>*/}

                    </ul>
                </Grid>

                <br/>
                <Divider/>

                <Grid item xs={12}><small>With Preferences</small></Grid>

                <Grid item xs={12}>
                    <ul className="tally-sheet-code-list">
                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PRE_34_PD;
                            let tallySheetCodeLabel = "Revised 30 PD";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "Revised 30 PV (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(electionId, tallySheetCode, subElectionId)}
                                >
                                    List
                                </Link>
                            </li>
                        })}
                        <li>Revised 30 ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_34_ED)}
                            >
                                List
                            </Link>
                        </li>
                        <li>Revised All Island
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PRE_34_AI)}
                            >
                                List
                            </Link>
                        </li>
                    </ul>
                </Grid>
            </Grid>

            <Grid item xs={4} className="election-grid">
                <Grid item xs={12}><h4>Release</h4></Grid>
                <Grid item xs={12}>
                    <ul className="tally-sheet-code-list">
                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PRE_30_PD;
                            let tallySheetCodeLabel = "PRE 30 PD";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PRE 30 PV (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_RESULTS_RELEASE(electionId, tallySheetCode, subElectionId)}
                                >
                                    List
                                </Link>
                            </li>
                        })}
                        <li>PRE 30 ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_RESULTS_RELEASE(electionId, TALLY_SHEET_CODE_PRE_30_ED)}
                            >
                                List
                            </Link>
                        </li>
                        <li>All Island ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_RESULTS_RELEASE(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS)}
                            >
                                List
                            </Link>
                        </li>
                        <li>All Island
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_RESULTS_RELEASE(electionId, TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS)}
                            >
                                List
                            </Link>
                        </li>
                    </ul>
                </Grid>
                <br/>
                <Divider/>

                <Grid item xs={12}><small>With Preferences</small></Grid>

                <Grid item xs={12}>
                    <ul className="tally-sheet-code-list">
                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PRE_34_PD;
                            let tallySheetCodeLabel = "Revised 30 PD";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "Revised 30 PV (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_RESULTS_RELEASE(electionId, tallySheetCode, subElectionId)}
                                >
                                    List
                                </Link>
                            </li>
                        })}
                        <li>Revised 30 ED
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_RESULTS_RELEASE(electionId, TALLY_SHEET_CODE_PRE_34_ED)}
                            >
                                List
                            </Link>
                        </li>

                        <li>Revised All Island
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_RESULTS_RELEASE(electionId, TALLY_SHEET_CODE_PRE_34_AI)}
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
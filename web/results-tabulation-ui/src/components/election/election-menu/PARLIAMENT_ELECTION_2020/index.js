import BreadCrumb from "../../../bread-crumb";
import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_DATA_ENTRY,
    PATH_ELECTION_REPORT, PATH_ELECTION_RESULTS_RELEASE
} from "../../../../App";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React from "react";

const TALLY_SHEET_CODE_CE_201 = "CE-201";
const TALLY_SHEET_CODE_CE_201_PV = "CE-201-PV";
const TALLY_SHEET_CODE_PE_27 = "PE-27";
const TALLY_SHEET_CODE_PE_4 = "PE-4";
const TALLY_SHEET_CODE_PE_CE_RO_V1 = "PE-CE-RO-V1";
const TALLY_SHEET_CODE_PE_R1 = "PE-R1";
const TALLY_SHEET_CODE_PE_CE_RO_V2 = "PE-CE-RO-V2";
const TALLY_SHEET_CODE_PE_R2 = "PE-R2";
const TALLY_SHEET_CODE_PE_CE_RO_PR_1 = "PE-CE-RO-PR-1";
const TALLY_SHEET_CODE_PE_CE_RO_PR_2 = "PE-CE-RO-PR-2";
const TALLY_SHEET_CODE_PE_CE_RO_PR_3 = "PE-CE-RO-PR-3";

export default function PARLIAMENT_ELECTION_2020(
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
                    let tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PE_27];
                    let tallySheetCodeLabels = ["CE 201", "PE-27"];
                    if (subElection.voteType === "Postal") {
                        tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PE_27];
                        tallySheetCodeLabels = ["CE 201 PV (Postal)", "PE-27 PV (Postal)"];
                    }
                    return <Grid item xs={12} key={subElectionId}>
                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_DATA_ENTRY(subElectionId, tallySheetCode)}
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
                    let tallySheetCodes = [TALLY_SHEET_CODE_PE_4];
                    let tallySheetCodeLabels = ["PE-4"];
                    if (subElection.voteType === "Postal") {
                        tallySheetCodes = [TALLY_SHEET_CODE_PE_4];
                        tallySheetCodeLabels = ["PE-4 PV (Postal)"];
                    }
                    return <Grid item xs={12} key={subElectionId}>
                        <Grid item xs={12}>
                            <ul className="tally-sheet-code-list">
                                {tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={tallySheetCodeIndex}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_DATA_ENTRY(subElectionId, tallySheetCode)}
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
                            let tallySheetCode = TALLY_SHEET_CODE_PE_CE_RO_V1;
                            let tallySheetCodeLabel = "PE-CE-RO-V1";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PE-CE-RO-V1 (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(subElectionId, tallySheetCode)}
                                >
                                    List
                                </Link>
                            </li>
                        })}

                        {subElections.map((subElection) => {
                            const subElectionId = subElection.electionId;
                            let tallySheetCode = TALLY_SHEET_CODE_PE_R1;
                            let tallySheetCodeLabel = "PE-R1";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PE-R1 (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(subElectionId, tallySheetCode)}
                                >
                                    List
                                </Link>
                            </li>
                        })}

                        <li>PE-CE-RO-V2
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PE_CE_RO_V2)}
                            >
                                List
                            </Link>
                        </li>

                        <li>PE-R2
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PE_R2)}
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
                            let tallySheetCode = TALLY_SHEET_CODE_PE_CE_RO_PR_1;
                            let tallySheetCodeLabel = "PE-CE-RO-PR-1";
                            if (subElection.voteType === "Postal") {
                                tallySheetCodeLabel = "PE-CE-RO-PR-1 (Postal)";
                            }

                            return <li key={subElectionId}>{tallySheetCodeLabel}
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_REPORT(subElectionId, tallySheetCode)}
                                >
                                    List
                                </Link>
                            </li>
                        })}

                        <li>PE-CE-RO-PR-2
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_2)}
                            >
                                List
                            </Link>
                        </li>

                        <li>PE-CE-RO-PR-3
                            <Link
                                className="tally-sheet-code-list-item btn-list"
                                to={PATH_ELECTION_REPORT(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_3)}
                            >
                                List
                            </Link>
                        </li>
                    </ul>
                </Grid>

            </Grid>

            <Grid item xs={4} className="election-grid">
                <Grid item xs={12}><h4>Release</h4></Grid>
            </Grid>

        </Grid>

    </div>
}
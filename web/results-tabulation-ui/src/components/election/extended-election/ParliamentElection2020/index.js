import Grid from "@material-ui/core/Grid";
import {
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
    TALLY_SHEET_CODE_PE_R1,
    TALLY_SHEET_CODE_PE_R2,
    TALLY_SHEET_CODE_PE_39,
    TALLY_SHEET_CODE_PE_22, TALLY_SHEET_CODE_PE_21
} from "./TALLY_SHEET_CODE";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React from "react";
import * as Settings from './settings'
import ExtendedElectionDefault from "../extended-election-default";
import ParliamentElection2020TallySheetEdit from "./tally-sheet-edit";

export default class ExtendedElectionParliamentElection2020 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, Settings.TALLY_SHEET_LIST_ACTIONS, ParliamentElection2020TallySheetEdit);
    }

    getElectionHome() {
        const {electionId, electionName} = this.election;
        const voteTypes = ["Postal", "NonPostal"];

        return <div className="page-content">
            <h1>{electionName}</h1>

            <Grid container spacing={3}>
                <Grid item xs={4} className="election-grid">

                    <Grid item xs={12}><h2>Data Entry</h2></Grid>

                    {voteTypes.map((voteType) => {
                        let tallySheetCodes = [];
                        let tallySheetCodeLabels = [];
                        if (voteType === "Postal") {
                            tallySheetCodes = [TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_39];
                            tallySheetCodeLabels = ["CE 201 PV (Postal)", "PE-27 PV (Postal)", "PE-39 (Postal)"];
                        } else if (voteType === "NonPostal") {
                            tallySheetCodes = [TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_PE_27, TALLY_SHEET_CODE_PE_39];
                            tallySheetCodeLabels = ["CE 201", "PE-27", "PE-39"];
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
                        let tallySheetCodes = [];
                        let tallySheetCodeLabels = [];
                        if (voteType === "Postal") {
                            tallySheetCodes = [TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22];
                            tallySheetCodeLabels = ["PE-4 PV (Postal)", "PE-22 (Postal)"];
                        } else if (voteType === "NonPostal") {
                            tallySheetCodes = [TALLY_SHEET_CODE_PE_4, TALLY_SHEET_CODE_PE_22];
                            tallySheetCodeLabels = ["PE-4", "PE-22"];
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
                <Grid item xs={4} className="election-grid">
                    <Grid item xs={12}><h2>Reports</h2></Grid>

                    <Grid item xs={12}>
                        <ul className="tally-sheet-code-list">
                            {voteTypes.map((voteType) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === "Postal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_V1];
                                    tallySheetCodeLabels = ["PE-CE-RO-V1 (Postal)"];
                                } else if (voteType === "NonPostal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_V1];
                                    tallySheetCodeLabels = ["PE-CE-RO-V1"];
                                }

                                return tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={voteType}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                        >
                                            List
                                        </Link>
                                    </li>
                                });
                            })}

                            {voteTypes.map((voteType) => {
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === "Postal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_R1];
                                    tallySheetCodeLabels = ["PE-R1 (Postal)"];
                                } else if (voteType === "NonPostal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_R1];
                                    tallySheetCodeLabels = ["PE-R1"];
                                }

                                return tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={voteType}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                        >
                                            List
                                        </Link>
                                    </li>
                                });
                            })}

                            <li>PE-CE-RO-V2
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_V2)}
                                >
                                    List
                                </Link>
                            </li>

                            <li>PE-R2
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_R2)}
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
                                let tallySheetCodes = [];
                                let tallySheetCodeLabels = [];
                                if (voteType === "Postal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_PR_1];
                                    tallySheetCodeLabels = ["PE-CE-RO-PR-1 (Postal)"];
                                } else if (voteType === "NonPostal") {
                                    tallySheetCodes = [TALLY_SHEET_CODE_PE_CE_RO_PR_1];
                                    tallySheetCodeLabels = ["PE-CE-RO-PR-1"];
                                }

                                return tallySheetCodes.map((tallySheetCode, tallySheetCodeIndex) => {
                                    return <li key={voteType}>{tallySheetCodeLabels[tallySheetCodeIndex]}
                                        <Link
                                            className="tally-sheet-code-list-item btn-list"
                                            to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType)}
                                        >
                                            List
                                        </Link>
                                    </li>
                                });
                            })}

                            <li>PE-CE-RO-PR-2
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_2)}
                                >
                                    List
                                </Link>
                            </li>

                            <li>PE-CE-RO-PR-3
                                <Link
                                    className="tally-sheet-code-list-item btn-list"
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_CE_RO_PR_3)}
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
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(electionId, TALLY_SHEET_CODE_PE_21)}
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
}

import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_RESULTS_RELEASE
} from "../../../../App";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PE_27,
    TALLY_SHEET_CODE_PE_4,
    TALLY_SHEET_CODE_PE_CE_RO_V1,
    TALLY_SHEET_CODE_PE_R1,
    TALLY_SHEET_CODE_PE_CE_RO_V2,
    TALLY_SHEET_CODE_PE_R2,
    TALLY_SHEET_CODE_PE_CE_RO_PR_1,
    TALLY_SHEET_CODE_PE_CE_RO_PR_2,
    TALLY_SHEET_CODE_PE_CE_RO_PR_3,
} from "./TALLy_SHEET_CODES";
import {Link} from "react-router-dom";
import Divider from "@material-ui/core/Divider";
import React from "react";
import * as Settings from './settings'
import {
    AREA_TYPE_COUNTING_CENTRE, AREA_TYPE_COUNTRY,
    AREA_TYPE_ELECTORAL_DISTRICT,
    AREA_TYPE_POLLING_DIVISION
} from "../../constants/AREA_TYPE";
import {VOTE_TYPE_POSTAL} from "../../constants/VOTE_TYPE";
import {getFirstOrNull} from "../../../../utils";


export const TALLY_SHEET_LIST_ACTIONS = Settings.TALLY_SHEET_LIST_ACTIONS;
export const TALLY_SHEET_LIST_COLUMNS = Settings.TALLY_SHEET_LIST_COLUMNS;

export const mapRequiredAreasToTallySheet = function (tallySheet) {
    if (tallySheet.area.areaType === AREA_TYPE_COUNTING_CENTRE) {
        if (tallySheet.election.voteType === VOTE_TYPE_POSTAL) {
            const countingCentre = tallySheet.area;
            const electoralDistrict = getFirstOrNull(countingCentre.electoralDistricts);
            tallySheet.countingCentre = countingCentre;
            tallySheet.electoralDistrict = electoralDistrict;
        } else {
            const countingCentre = tallySheet.area;
            const pollingStation = getFirstOrNull(countingCentre.pollingStations);
            const pollingDistrict = getFirstOrNull(pollingStation.pollingDistricts);
            const pollingDivision = getFirstOrNull(pollingDistrict.pollingDivisions);
            const electoralDistrict = getFirstOrNull(pollingDivision.electoralDistricts);
            tallySheet.countingCentre = countingCentre;
            tallySheet.pollingDivision = pollingDivision;
            tallySheet.electoralDistrict = electoralDistrict;
        }
    } else if (tallySheet.area.areaType === AREA_TYPE_POLLING_DIVISION) {
        const pollingDivision = tallySheet.area;
        const electoralDistrict = getFirstOrNull(pollingDivision.electoralDistricts);
        tallySheet.pollingDivision = pollingDivision;
        tallySheet.electoralDistrict = electoralDistrict;
    } else if (tallySheet.area.areaType === AREA_TYPE_ELECTORAL_DISTRICT) {
        tallySheet.electoralDistrict = tallySheet.area;
    } else if (tallySheet.area.areaType === AREA_TYPE_COUNTRY) {
        tallySheet.country = tallySheet.area;
    }

    return tallySheet;
};

export const ElectionHome = function (
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
                                            to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
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
                                            to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
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
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
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
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
                                >
                                    List
                                </Link>
                            </li>
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
                                    to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
                                >
                                    List
                                </Link>
                            </li>
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

            </Grid>

            <Grid item xs={4} className="election-grid">
                <Grid item xs={12}><h4>Release</h4></Grid>
            </Grid>

        </Grid>

    </div>
}
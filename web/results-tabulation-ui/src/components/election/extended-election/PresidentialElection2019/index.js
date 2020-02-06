import Grid from "@material-ui/core/Grid";
import {
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_RESULTS_RELEASE
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
import {getFirstOrNull} from "../../../../utils";
import {
    AREA_TYPE_COUNTING_CENTRE,
    AREA_TYPE_COUNTRY,
    AREA_TYPE_ELECTORAL_DISTRICT,
    AREA_TYPE_POLLING_DIVISION
} from "../../constants/AREA_TYPE";
import {VOTE_TYPE_POSTAL} from "../../constants/VOTE_TYPE";
import ExtendedElectionDefault from "../extended-election-default";
import PresidentialElection2019TallySheetEdit from "./tally-sheet-edit";

export default class ExtendedElectionPresidentialElection2019 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, Settings.TALLY_SHEET_LIST_ACTIONS, PresidentialElection2019TallySheetEdit);
    }

    getElectionHome() {
        const {electionId, electionName, subElections} = this.election;

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
                                let tallySheetCode = TALLY_SHEET_CODE_PRE_30_PD;
                                let tallySheetCodeLabel = "PRE 30 PD";
                                if (subElection.voteType === "Postal") {
                                    tallySheetCodeLabel = "PRE 30 PV (Postal)";
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
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
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
                                        to={PATH_ELECTION_TALLY_SHEET_LIST(subElectionId, tallySheetCode)}
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
                                        to={PATH_ELECTION_RESULTS_RELEASE(subElectionId, tallySheetCode)}
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
                                        to={PATH_ELECTION_RESULTS_RELEASE(subElectionId, tallySheetCode)}
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

    mapRequiredAreasToTallySheet(tallySheet) {
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
    }
}

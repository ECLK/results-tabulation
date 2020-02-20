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
    TALLY_SHEET_CODE_PE_R2
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
import ParliamentElection2020TallySheetEdit from "./tally-sheet-edit";
import {AreaEntity} from "../../../../services/tabulation-api/entities/area.entity";

export default class ExtendedElectionParliamentElection2020 extends ExtendedElectionDefault {

    constructor(election) {
        super(election, Settings.TALLY_SHEET_LIST_COLUMNS, Settings.TALLY_SHEET_LIST_ACTIONS, ParliamentElection2020TallySheetEdit);
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

    async mapRequiredAreasToTallySheet(tallySheet) {
        const areaEntity = new AreaEntity();

        if (tallySheet.area.areaType === AREA_TYPE_COUNTING_CENTRE) {
            let countingCentre = null;
            let pollingStation = null;
            let pollingDistrict = null;
            let pollingDivision = null;
            let electoralDistrict = null;

            if (tallySheet.area) {
                const countingCentreId = tallySheet.area.areaId;
                countingCentre = await areaEntity.getById(countingCentreId);
            }

            if (countingCentre) {
                const pollingStationId = getFirstOrNull(countingCentre.pollingStationIds);
                pollingStation = await areaEntity.getById(pollingStationId);
            }

            if (pollingStation) {
                const pollingDistrictId = getFirstOrNull(pollingStation.pollingDistrictIds);
                pollingDistrict = await areaEntity.getById(pollingDistrictId);
            }

            if (pollingDistrict) {
                const pollingDivisionId = getFirstOrNull(pollingDistrict.pollingDivisionIds);
                pollingDivision = await areaEntity.getById(pollingDivisionId);
            }

            if (pollingDivision) {
                const electoralDistrictId = getFirstOrNull(pollingDivision.electoralDistrictIds);
                electoralDistrict = await areaEntity.getById(electoralDistrictId);
            }

            tallySheet.countingCentre = countingCentre;
            tallySheet.pollingDivision = pollingDivision;
            tallySheet.electoralDistrict = electoralDistrict;
        } else if (tallySheet.area.areaType === AREA_TYPE_POLLING_DIVISION) {
            let pollingDivision = null;
            let electoralDistrict = null;

            if (tallySheet.area) {
                const pollingDivisionId = tallySheet.area.areaId;
                pollingDivision = await areaEntity.getById(pollingDivisionId);
            }

            if (pollingDivision) {
                const electoralDistrictId = getFirstOrNull(pollingDivision.electoralDistrictIds);
                electoralDistrict = await areaEntity.getById(electoralDistrictId);
            }

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

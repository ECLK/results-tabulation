import React, {Component, useEffect, useState} from "react";
import {Link} from 'react-router-dom';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

import {
    getTallySheet,
    TALLY_SHEET_STATUS_ENUM,
    getTallySheetProof
} from "../../services/tabulation-api";
import {
    PATH_ELECTION,
    PATH_ELECTION_BY_ID,
    PATH_ELECTION_RESULTS_RELEASE_VIEW
} from "../../App";
import {
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_34_ED
} from "../../components/election/election-menu/PRESIDENTIAL_ELECTION_2019/TALLy_SHEET_CODES";
import Processing from "../../components/processing";
import Error from "../../components/error";
import BreadCrumb from "../../components/bread-crumb";
import Button from "@material-ui/core/Button";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import TextField from "@material-ui/core/TextField/TextField";
import {fieldMatch} from "../../utils";
import {getAreaName} from "../../utils/tallySheet";
import PrintLetterButton from "../../components/tally-sheet/print-letter-button";


export default function ReleaseList({history, queryString, election}) {
    const {electionId, electionName} = election;
    const {tallySheetCode} = queryString;

    const [tallySheets, setTallySheets] = useState([]);
    const [proofStatuses, setProofStatuses] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    const [searchParameters, setSearchParameters] = React.useState({
        electoralDistrict: '',
        pollingDivision: '',
        countingCentre: '',
        status: ''
    });

    const handleChange = name => event => {
        setSearchParameters({...searchParameters, [name]: event.target.value});
    };

    function getElection() {
        return election;
    }

    const fetchProofStatuses = async () => {
        const proofStatuses = [];
        for (var i = 0; i < tallySheets.length; i++) {
            const {submissionProofId} = tallySheets[i];
            const proofStates = await getTallySheetProof(submissionProofId);
            proofStatuses[i] = proofStates;
            setProofStatuses([...proofStatuses]);
        }
    }


    useEffect(() => {
        getTallySheet({
            electionId: getElection().electionId,
            tallySheetCode,
            limit: 3000,
            offset: 0
        }).then((tallySheets) => {
            setTallySheets(tallySheets);
            setProcessing(false);
        }).catch((error) => {
            setError(true);
            setProcessing(false);
        })
    }, [])

    useEffect(() => {
        fetchProofStatuses();
    }, [tallySheets])


    function getTallySheetListJsx() {
        if (processing) {
            return <Processing/>
        } else if (error) {
            return <Error
                title="Tally sheet list cannot be accessed"
            />
        } else {
            if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_PD || tallySheetCode === TALLY_SHEET_CODE_PRE_34_PD) {
                return getTallySheetListJsx_PRE_30_PD(tallySheets)
            } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_ED || tallySheetCode === TALLY_SHEET_CODE_PRE_34_ED) {
                return getTallySheetListJsx_PRE_30_ED(tallySheets)
            } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS || TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS) {
                return getTallySheetListJsx_AllIslandReports(tallySheets)
            }
        }
    }

    function getActions(tallySheet, proofStates) {
        const released = proofStates && proofStates.finished;
        const uploaded = proofStates && proofStates.scannedFiles.length > 0;
        const loading = !proofStates;
        const verified = tallySheet.tallySheetStatus === TALLY_SHEET_STATUS_ENUM.VERIFIED;
        return <TableCell align="center">
            <Button
                variant="outlined" color="default"
                size="small"
                onClick={() => history.push(PATH_ELECTION_RESULTS_RELEASE_VIEW(electionId, tallySheet.tallySheetId))}
                disabled={!verified}
            >
                View
            </Button>
            <PrintLetterButton
                variant="outlined" color="default"
                size="small"
                disabled={!verified}
                onClick={() => {
                }}
                tallySheetId={tallySheet.tallySheetId}
                tallySheetVersionId={tallySheet.lockedVersionId}
            >
                Print Letter
            </PrintLetterButton>
            <Button
                variant="outlined" color="default"
                size="small"
                disabled={loading || !verified || released}
                onClick={() => history.push(PATH_ELECTION_RESULTS_RELEASE_VIEW(electionId, tallySheet.tallySheetId))}
            >
                Upload Proof
            </Button>
            <Button
                variant="outlined" color="default"
                disabled={!tallySheet.locked || tallySheet.notified}
                size="small"
                onClick={() => history.push(PATH_ELECTION_RESULTS_RELEASE_VIEW(electionId, tallySheet.tallySheetId))}

            >
                Notify
            </Button>
            <Button
                variant="outlined" color="default"
                disabled={!tallySheet.locked || tallySheet.released}
                size="small"
                onClick={() => history.push(PATH_ELECTION_RESULTS_RELEASE_VIEW(electionId, tallySheet.tallySheetId))}

            >
                Release
            </Button>
        </TableCell>
    }


    function getTallySheetListJsx_PRE_30_PD(tallySheets) {
        const tbody = [];
        for (var i = 0; i < tallySheets.length; i++) {
            const tallySheet = tallySheets[i];
            const proofStates = proofStatuses[i];
            if (fieldMatch(getAreaName(tallySheet.electoralDistrict), searchParameters.electoralDistrict) &&
                fieldMatch(modifyStateForReleaseView(tallySheet, proofStates), searchParameters.status) &&
                fieldMatch(getAreaName(tallySheet.pollingDivision), searchParameters.pollingDivision)) {
                tbody.push(<TableRow key={tallySheet.tallySheetId}>
                    <TableCell align="left">{getAreaName(tallySheet.electoralDistrict)}</TableCell>
                    <TableCell align="left">{getAreaName(tallySheet.pollingDivision)}</TableCell>
                    <TableCell align="center">{modifyStateForReleaseView(tallySheet, proofStates)}</TableCell>
                    {getActions(tallySheet, proofStates)}
                </TableRow>);
            }
        }

        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell align="center" style={{width: "20%"}}>
                        <TextField
                            value={searchParameters.electoralDistrict}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Electoral District"
                            onChange={handleChange('electoralDistrict')}
                        />
                    </TableCell>
                    <TableCell align="center" style={{width: "20%"}}>
                        <TextField
                            value={searchParameters.pollingDivision}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Polling Division"
                            onChange={handleChange('pollingDivision')}
                        />
                    </TableCell>
                    <TableCell align="center" style={{width: "10%"}}>
                        <TextField
                            value={searchParameters.status}
                            margin="dense"
                            variant="outlined"
                            placeholder="Status"
                            onChange={handleChange('status')}
                        />
                    </TableCell>
                    <TableCell align="left"></TableCell>
                    <TableCell align="center"></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell align="left">Electoral District</TableCell>
                    <TableCell align="left">Polling Division</TableCell>
                    <TableCell align="center">Status</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tbody}
            </TableBody>
        </Table>
    }

    function modifyStateForReleaseView(tallySheet, proof) {
        let status = tallySheet.tallySheetStatus;
        if (status !== TALLY_SHEET_STATUS_ENUM.VERIFIED) {
            return "Not Verified";
        }
        if (proof && proof.finished) {
            return "Released";
        }
        return status + (proof ? "" : " (loading)");
    }

    function getTallySheetListJsx_PRE_30_ED(tallySheets) {
        const tbody = [];
        for (var i = 0; i < tallySheets.length; i++) {
            const tallySheet = tallySheets[i];
            const proofStates = proofStatuses[i];
            if (fieldMatch(getAreaName(tallySheet.electoralDistrict), searchParameters.electoralDistrict) &&
                fieldMatch(modifyStateForReleaseView(tallySheet, proofStates), searchParameters.status)) {
                tbody.push(<TableRow key={tallySheet.tallySheetId}>
                    <TableCell align="left">{getAreaName(tallySheet.electoralDistrict)}</TableCell>
                    <TableCell align="center">{modifyStateForReleaseView(tallySheet, proofStates)}</TableCell>
                    {getActions(tallySheet, proofStates)}
                </TableRow>);
            }
        }

        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell align="center" style={{width: "20%"}}>
                        <TextField
                            value={searchParameters.electoralDistrict}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Electoral District"
                            onChange={handleChange('electoralDistrict')}
                        />
                    </TableCell>
                    <TableCell align="center" style={{width: "10%"}}>
                        <TextField
                            value={searchParameters.status}
                            margin="dense"
                            variant="outlined"
                            placeholder="Status"
                            onChange={handleChange('status')}
                        />
                    </TableCell>
                    <TableCell align="left"></TableCell>
                    <TableCell align="center"></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell align="left">Electoral District</TableCell>
                    <TableCell align="center">Status</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tbody}
            </TableBody>
        </Table>
    }

    function getTallySheetListJsx_AllIslandReports(tallySheets) {
        const tbody = [];
        for (var i = 0; i < tallySheets.length; i++) {
            const tallySheet = tallySheets[i];
            const proofStates = proofStatuses[i];
            tbody.push(<TableRow key={tallySheet.tallySheetId}>
                <TableCell align="left">{getAreaName(tallySheet.country)}</TableCell>
                <TableCell align="center">{modifyStateForReleaseView(tallySheet, proofStates)}</TableCell>
                {getActions(tallySheet, proofStates)}
            </TableRow>);
        }

        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell align="left">Country</TableCell>
                    <TableCell align="center">Status</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tbody}
            </TableBody>
        </Table>
    }

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: electionName, to: PATH_ELECTION_BY_ID(electionId)},
                {
                    label: getTallySheetCodeStr({tallySheetCode, election: getElection()}).toLowerCase() + " release",
                    to: PATH_ELECTION_BY_ID(electionId)
                    // TODO: should be PATH_ELECTION_RESULTS_RELEASE(electionId, tallySheetCode)
                },
            ]}
        />
        <div className="page-content">
            <div>{electionName}</div>
            <div>{getTallySheetCodeStr({tallySheetCode, election: getElection()})}</div>
            {getTallySheetListJsx()}
        </div>
    </div>
}



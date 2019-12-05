import React, {useEffect, useState} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import {getTallySheet, TALLY_SHEET_STATUS_ENUM} from "../../services/tabulation-api";
import {
    PATH_ELECTION,
    PATH_ELECTION_BY_ID,
    PATH_ELECTION_DATA_ENTRY,
    PATH_ELECTION_DATA_ENTRY_EDIT,
    PATH_ELECTION_REPORT,
    PATH_ELECTION_REPORT_VIEW,
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD,
    TALLY_SHEET_CODE_PRE_34_I_RO,
    TALLY_SHEET_CODE_PRE_34_II_RO,
    TALLY_SHEET_CODE_PRE_34,
    TALLY_SHEET_CODE_PRE_41,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_34_ED, TALLY_SHEET_CODE_PRE_34_AI
} from "../../App";
import Processing from "../../components/processing";
import BreadCrumb from "../../components/bread-crumb";
import Button from "@material-ui/core/Button";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import TextField from "@material-ui/core/TextField/TextField";
import {fieldMatch} from "../../utils";
import {getAreaName} from "../../utils/tallySheet";

export default function ReportList({history, queryString, election, subElection}) {
    const {electionId, electionName} = election;
    const {tallySheetCode} = queryString;

    const [tallySheets, setTallySheets] = useState([]);
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
        return subElection ? subElection : election;
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

    function getTallySheetListJsx() {
        if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_PD || tallySheetCode === TALLY_SHEET_CODE_PRE_34_I_RO || tallySheetCode === TALLY_SHEET_CODE_PRE_34_PD) {
            return getTallySheetListJsx_PRE_30_PD(tallySheets)
        } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_ED || tallySheetCode === TALLY_SHEET_CODE_PRE_34_II_RO ||
            tallySheetCode === TALLY_SHEET_CODE_PRE_34 || tallySheetCode === TALLY_SHEET_CODE_PRE_34_ED) {
            return getTallySheetListJsx_PRE_30_ED(tallySheets)
        } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS ||
            tallySheetCode === TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS || tallySheetCode === TALLY_SHEET_CODE_PRE_34_AI) {
            return getTallySheetListJsx_AllIslandReports(tallySheets)
        }
    }

    function getActions(tallySheet) {
        return <TableCell align="center">
            <Button
                variant="outlined" color="default"
                size="small"
                disabled={!(tallySheet.tallySheetStatus !== TALLY_SHEET_STATUS_ENUM.VERIFIED)}

                onClick={() => history.push(PATH_ELECTION_REPORT_VIEW(electionId, tallySheet.tallySheetId))}
            >
                Verify
            </Button>
            <Button
                variant="outlined" color="default"
                size="small"
                onClick={() => history.push(PATH_ELECTION_REPORT_VIEW(electionId, tallySheet.tallySheetId))}
            >
                View
            </Button>
            <Button
                variant="outlined" color="default"
                disabled={!(tallySheet.tallySheetStatus === TALLY_SHEET_STATUS_ENUM.VERIFIED)}
                size="small"
                onClick={() => history.push(PATH_ELECTION_REPORT_VIEW(electionId, tallySheet.tallySheetId))}
            >
                Unlock
            </Button>
        </TableCell>
    }

    function getTallySheetListJsx_PRE_30_PD(tallySheets) {
        let tallySheetRows = [];
        if (processing) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={4} align="center">
                    <Processing/>
                </TableCell>
            </TableRow>
        } else if (!tallySheets || error) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={4} align="center">
                    Tally sheet list cannot be accessed
                </TableCell>
            </TableRow>
        } else if (tallySheets) {
            if (tallySheets.length === 0) {
                tallySheetRows = <TableRow>
                    <TableCell colSpan={4} align="center">No reports available or authorized to access.</TableCell>
                </TableRow>
            } else {
                for (let i = 0; i < tallySheets.length; i++) {
                    const tallySheet = tallySheets[i];
                    if (fieldMatch(getAreaName(tallySheet.electoralDistrict), searchParameters.electoralDistrict) &&
                        fieldMatch(tallySheet.tallySheetStatus, searchParameters.status) &&
                        fieldMatch(getAreaName(tallySheet.pollingDivision), searchParameters.pollingDivision)) {
                        tallySheetRows.push(<TableRow key={tallySheet.tallySheetId}>
                            <TableCell align="left">{getAreaName(tallySheet.electoralDistrict)}</TableCell>
                            <TableCell align="left">{getAreaName(tallySheet.pollingDivision)}</TableCell>
                            <TableCell align="center">{tallySheet.tallySheetStatus}</TableCell>
                            {getActions(tallySheet)}
                        </TableRow>)
                    }
                }
            }
        }

        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell align="center">
                        <TextField
                            style={{width: "100%"}}
                            value={searchParameters.electoralDistrict}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Electoral District"
                            onChange={handleChange('electoralDistrict')}
                        />
                    </TableCell>
                    <TableCell align="center">
                        <TextField
                            style={{width: "100%"}}
                            value={searchParameters.pollingDivision}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Polling Division"
                            onChange={handleChange('pollingDivision')}
                        />
                    </TableCell>
                    <TableCell align="center">
                        <TextField
                            style={{width: "100%"}}
                            value={searchParameters.status}
                            margin="dense"
                            variant="outlined"
                            placeholder="Status"
                            onChange={handleChange('status')}
                        />
                    </TableCell>
                    <TableCell align="left"> </TableCell>
                    <TableCell align="center"> </TableCell>
                </TableRow>
                <TableRow>
                    <TableCell align="left">Electoral District</TableCell>
                    <TableCell align="left">Polling Division</TableCell>
                    <TableCell align="center">Status</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tallySheetRows}
            </TableBody>
        </Table>
    }


    function getTallySheetListJsx_PRE_30_ED(tallySheets) {
        let tallySheetRows = [];
        if (processing) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={3} align="center">
                    <Processing/>
                </TableCell>
            </TableRow>
        } else if (!tallySheetRows || error) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={3} align="center">
                    Tally sheet list cannot be accessed
                </TableCell>
            </TableRow>
        } else if (tallySheets) {
            if (tallySheets.length === 0) {
                tallySheetRows = <TableRow>
                    <TableCell colSpan={3} align="center">No reports available or authorized to access.</TableCell>
                </TableRow>
            } else {
                for (let i = 0; i < tallySheets.length; i++) {
                    const tallySheet = tallySheets[i];
                    if (fieldMatch(getAreaName(tallySheet.electoralDistrict), searchParameters.electoralDistrict) &&
                        fieldMatch(tallySheet.tallySheetStatus, searchParameters.status)) {
                        tallySheetRows.push(<TableRow key={tallySheet.tallySheetId}>
                            <TableCell align="left">{getAreaName(tallySheet.electoralDistrict)}</TableCell>
                            <TableCell align="center">{tallySheet.tallySheetStatus}</TableCell>
                            {getActions(tallySheet)}
                        </TableRow>)
                    }
                }
            }
        }


        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell align="center">
                        <TextField
                            style={{width: "100%"}}
                            value={searchParameters.electoralDistrict}
                            margin="dense"
                            variant="outlined"
                            placeholder="Search Electoral District"
                            onChange={handleChange('electoralDistrict')}
                        />
                    </TableCell>
                    <TableCell align="center">
                        <TextField
                            style={{width: "100%"}}
                            value={searchParameters.status}
                            margin="dense"
                            variant="outlined"
                            placeholder="Status"
                            onChange={handleChange('status')}
                        />
                    </TableCell>
                    <TableCell align="left"></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell align="left">Electoral District</TableCell>
                    <TableCell align="center">Status</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tallySheetRows}
            </TableBody>
        </Table>
    }

    function getTallySheetListJsx_AllIslandReports(tallySheets) {
        let tallySheetRows = [];
        if (processing) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={3} align="center">
                    <Processing/>
                </TableCell>
            </TableRow>
        } else if (!tallySheetRows || error) {
            tallySheetRows = <TableRow>
                <TableCell colSpan={3} align="center">
                    Tally sheet list cannot be accessed
                </TableCell>
            </TableRow>
        } else if (tallySheets) {
            if (tallySheets.length === 0) {
                tallySheetRows = <TableRow>
                    <TableCell colSpan={3} align="center">No reports available or authorized to access.</TableCell>
                </TableRow>
            } else {
                for (let i = 0; i < tallySheets.length; i++) {
                    const tallySheet = tallySheets[i];
                    tallySheetRows.push(<TableRow key={tallySheet.tallySheetId}>
                        <TableCell align="left">{getAreaName(tallySheet.country)}</TableCell>
                        <TableCell align="center">{tallySheet.tallySheetStatus}</TableCell>
                        {getActions(tallySheet)}
                    </TableRow>)
                }
            }
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
                {tallySheetRows}
            </TableBody>
        </Table>
    }

    const tallySheetCodeStr = getTallySheetCodeStr({tallySheetCode, election: getElection()});

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: electionName, to: PATH_ELECTION_BY_ID(electionId)},
                {
                    label: tallySheetCodeStr.toLowerCase(),
                    to: PATH_ELECTION_REPORT(electionId, tallySheetCode)
                },
            ]}
        />
        <div className="page-content">
            <div>{electionName}</div>
            <div>{tallySheetCodeStr}</div>
            {getTallySheetListJsx()}
        </div>
    </div>
}


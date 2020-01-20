import React, {useEffect, useState} from "react";
import {getTallySheet} from "../../../services/tabulation-api";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {getAreaName, getTallySheetCodeStr} from "../../../utils/tallySheet";
import {
    PATH_ELECTION,
    PATH_ELECTION_BY_ID, PATH_ELECTION_DATA_ENTRY
} from "../../../App";
import Processing from "../../processing";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TextField from "@material-ui/core/TextField/TextField";
import TableBody from "@material-ui/core/TableBody";
import BreadCrumb from "../../bread-crumb";
import TallySheetListRow from "./tally-sheet-list-row";
import {TALLY_SHEET_LIST_ROW_ACTION} from "./tally-sheet-list-row-action";

export const TALLY_SHEET_LIST_COLUMN = {
    TALLY_SHEET_LIST_COLUMN_STATUS: "TALLY_SHEET_LIST_COLUMN_STATUS",
    TALLY_SHEET_LIST_COLUMN_ACTIONS: "TALLY_SHEET_LIST_COLUMN_ACTIONS",
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT: "TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT",
    TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION: "TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION",
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE: "TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE"
};

export const TALLY_SHEET_LIST_COLUMN_LABEL = {
    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_STATUS]: "Status",
    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ACTIONS]: "Actions",
    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT]: "Electoral District",
    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION]: "Polling Division",
    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE]: "Counting Centre"
}


export default function TallySheetList(
    {
        history,
        tallySheetCode,
        election,
        columns = [
            TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        actions = [
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VIEW,
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_UNLOCK
        ]
    }
) {
    const {electionId, electionName, rootElectionId, rootElection} = election;

    const [tallySheetListRows, setTallySheetListRows] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    const [searchParameters, setSearchParameters] = React.useState({});

    const handleChange = name => event => {
        setSearchParameters({...searchParameters, [name]: event.target.value});
    };


    useEffect(() => {
        columns.filter((column) => {
            setSearchParameters({...searchParameters, [column]: ""})
        });
    }, []);

    useEffect(() => {
        getTallySheet({
            electionId: electionId,
            tallySheetCode,
            limit: 3000, //TODO fix
            offset: 0
        }).then((tallySheets) => {
            debugger;
            setTallySheetListRows(tallySheets.map((tallySheet) => {
                return {
                    ...tallySheet,
                    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE]: tallySheet.countingCentre,
                    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION]: tallySheet.pollingDivision,
                    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT]: tallySheet.electoralDistrict,
                    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_STATUS]: tallySheet.tallySheetStatus,
                    [TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ACTIONS]: []
                }
            }));
            setProcessing(false);
        }).catch((error) => {
            setError(true);
            setProcessing(false);
        })
    }, []);


    function getTallySheetListJsx() {
        debugger;

        let tallySheetListJsx = [];

        if (processing) {
            tallySheetListJsx = <TableRow>
                <TableCell colSpan={5} align="center">
                    <Processing/>
                </TableCell>
            </TableRow>
        } else if (!tallySheetListRows || error) {
            tallySheetListJsx = <TableRow>
                <TableCell colSpan={5} align="center">
                    Tally sheet list cannot be accessed
                </TableCell>
            </TableRow>
        } else if (tallySheetListRows) {
            if (tallySheetListRows.length === 0) {
                tallySheetListJsx = <TableRow>
                    <TableCell colSpan={5} align="center">No tally sheets available or authorized to access.</TableCell>
                </TableRow>
            } else {
                for (let i = 0; i < tallySheetListRows.length; i++) {
                    const tallySheetListRow = tallySheetListRows[i];
                    tallySheetListJsx.push(<TallySheetListRow
                        tallySheetListRow={tallySheetListRow} history={history} electionId={electionId}
                        actions={actions} columns={columns}
                    />)
                }
            }
        }


        return <Table aria-label="simple table">
            <TableHead>
                <TableRow>
                    {columns.map((column) => {

                        return <TableCell align="center">
                            <TextField
                                style={{width: "100%"}}
                                value={searchParameters.electoralDistrict}
                                margin="dense"
                                variant="outlined"
                                placeholder={TALLY_SHEET_LIST_COLUMN_LABEL[column]}
                                onChange={handleChange('electoralDistrict')}
                            />
                        </TableCell>
                    })}
                </TableRow>
                <TableRow>
                    {columns.map((column) => {
                        return <TableCell align="center">{TALLY_SHEET_LIST_COLUMN_LABEL[column]}</TableCell>
                    })}
                </TableRow>
            </TableHead>
            <TableBody>
                {tallySheetListJsx}
            </TableBody>
        </Table>
    }

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: rootElection.electionName, to: PATH_ELECTION_BY_ID(rootElectionId)},
                {
                    label: getTallySheetCodeStr({tallySheetCode, election: election}).toLowerCase(),
                    to: PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, election.electionId)
                },
            ]}
        />
        <div className="page-content">
            <div>{rootElection.electionName}</div>
            <div>{getTallySheetCodeStr({tallySheetCode, election: election})}</div>
            {getTallySheetListJsx()}
        </div>
    </div>
}



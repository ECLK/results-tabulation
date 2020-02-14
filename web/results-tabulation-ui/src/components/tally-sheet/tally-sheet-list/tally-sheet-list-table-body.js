import React, {useEffect, useState} from "react";
import {getTallySheet} from "../../../services/tabulation-api";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {getTallySheetCodeStr} from "../../../utils/tallySheet";
import {
    PATH_ELECTION,
    PATH_ELECTION_BY_ID, PATH_ELECTION_TALLY_SHEET_LIST
} from "../../../App";
import Processing from "../../processing";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TextField from "@material-ui/core/TextField/TextField";
import TableBody from "@material-ui/core/TableBody";
import BreadCrumb from "../../bread-crumb";
import TallySheetListRow from "./tally-sheet-list-row";
import {
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
    TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../constants/TALLY_SHEET_ACTION";
import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE,
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_LABEL, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_VALUE_KEY
} from "../constants/TALLY_SHEET_COLUMN";


export default function TallySheetListTableBody(
    {
        history,
        tallySheetCode,
        election,
        columns = [
            TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        columnMetaMap = {},
        actions = [
            TALLY_SHEET_LIST_ROW_ACTION_VIEW,
            TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
            TALLY_SHEET_LIST_ROW_ACTION_UNLOCK
        ]
    }
) {
    const {electionId} = election;

    const [tallySheetListRows, setTallySheetListRows] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);


    useEffect(() => {
        getTallySheet({
            electionId: electionId,
            tallySheetCode,
            limit: 3000, //TODO fix
            offset: 0
        }).then((tallySheets) => {
            setTallySheetListRows(tallySheets.map((tallySheet) => {
                tallySheet = {...tallySheet};

                // Append the values for columns.
                columns.map((column) => {
                    let columnValue = tallySheet[TALLY_SHEET_LIST_COLUMN_VALUE_KEY[column]];
                    if (!columnValue) {
                        columnValue = "";
                    }

                    // If the value is an area object, assign areaName as the value.
                    if (typeof columnValue === "object" && columnValue.areaName) {
                        columnValue = columnValue.areaName;
                    }

                    tallySheet[column] = columnValue;
                });

                return tallySheet;

            }));
            setProcessing(false);
        }).catch((error) => {
            setError(true);
            setProcessing(false);
        })
    }, []);

    const getTallySheetListJsx = function () {
        return tallySheetListRows.map((tallySheetListRow, tallySheetListRowIndex) => (<TallySheetListRow
            key={tallySheetListRowIndex}
            tallySheetListRow={tallySheetListRow} history={history} electionId={electionId}
            actions={actions} columns={columns}
            columnMetaMap={columnMetaMap}
        />))
    };

    let tableBody = [];
    if (processing) {
        tableBody = <TableRow>
            <TableCell colSpan={5} align="center">
                <Processing/>
            </TableCell>
        </TableRow>
    } else if (!tallySheetListRows || error) {
        tableBody = <TableRow>
            <TableCell colSpan={5} align="center">
                Tally sheet list cannot be accessed
            </TableCell>
        </TableRow>
    } else if (tallySheetListRows) {
        if (tallySheetListRows.length === 0) {
            tableBody = <TableRow>
                <TableCell colSpan={5} align="center">No tally sheets available or authorized to
                    access.</TableCell>
            </TableRow>
        } else {
            tableBody = getTallySheetListJsx();
        }
    }

    return <TableBody>
        {tableBody}
    </TableBody>

}

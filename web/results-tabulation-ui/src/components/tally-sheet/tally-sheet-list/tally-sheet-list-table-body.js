import React, {useEffect, useState} from "react";
import {getTallySheet} from "../../../services/tabulation-api";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Processing from "../../processing";
import TableBody from "@material-ui/core/TableBody";
import TallySheetListRow from "./tally-sheet-list-row";
import {
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
    TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../constants/TALLY_SHEET_ACTION";
import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_LABEL,
    TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_VALUE
} from "../constants/TALLY_SHEET_COLUMN";


export default function TallySheetListTableBody(
    {
        history,
        tallySheetCode,
        voteType,
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

    function appendColumnValuesToTallySheetRow(tallySheet) {
        // Append the values for columns.
        for (let columnIndex = 0; columnIndex < columns.length; columnIndex++) {
            const column = columns[columnIndex];
            let columnValue = TALLY_SHEET_LIST_COLUMN_VALUE[column](tallySheet);
            if (!columnValue) {
                columnValue = "";
            }

            // If the value is an area object, assign areaName as the value.
            if (typeof columnValue === "object" && columnValue.areaName) {
                columnValue = columnValue.areaName;
            }

            tallySheet[column] = columnValue;
        }

        return tallySheet;
    }


    useEffect(() => {
        getTallySheet({electionId, tallySheetCode, voteType}).then((tallySheets) => {
            setTallySheetListRows(tallySheets.map((tallySheet) => {
                let _tallySheetListRow = {...tallySheet};
                _tallySheetListRow = appendColumnValuesToTallySheetRow(_tallySheetListRow);

                return _tallySheetListRow;

            }));
            setProcessing(false);
        }).catch((error) => {
            console.log(error.stack);
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
            onTallySheetUpdate={(_tallySheetListRow) => {
                _tallySheetListRow = appendColumnValuesToTallySheetRow(_tallySheetListRow);
                setTallySheetListRows((_tallySheetListRows) => {
                    Object.assign(_tallySheetListRows[tallySheetListRowIndex], _tallySheetListRow);
                    return [..._tallySheetListRows];
                })
            }}
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

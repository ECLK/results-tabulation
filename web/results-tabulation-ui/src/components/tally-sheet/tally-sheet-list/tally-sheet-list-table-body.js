import React, {useContext, useEffect, useState} from "react";
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
import {TallySheetContext} from "../../../services/tally-sheet.provider";


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
    const {getTallySheet} = useContext(TallySheetContext);

    const {electionId} = election;

    const [tallySheetListRows, setTallySheetListRows] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);


    useEffect(() => {
        getTallySheet({electionId, tallySheetCode, voteType}).then((tallySheets) => {
            setTallySheetListRows(tallySheets);
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
            tallySheetId={tallySheetListRow.tallySheetId} history={history} electionId={electionId}
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

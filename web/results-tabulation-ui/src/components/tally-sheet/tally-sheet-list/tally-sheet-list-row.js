import React from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
    TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../constants/TALLY_SHEET_ACTION";
import TallySheetListRowAction from "./tally-sheet-list-row-action";
import {TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_STATUS} from "../constants/TALLY_SHEET_COLUMN";


export default function TallySheetListRow(
    {
        history,
        electionId,
        tallySheetListRow,
        columns = [
            TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        actions = [
            TALLY_SHEET_LIST_ROW_ACTION_VIEW,
            TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
            TALLY_SHEET_LIST_ROW_ACTION_UNLOCK
        ]
    }
) {

    return <TableRow key={tallySheetListRow.tallySheetId}>
        {columns.map((column) => {
            if (column == TALLY_SHEET_LIST_COLUMN_ACTIONS) {
                return actions.map((action) => {
                    return <TallySheetListRowAction
                        electionId={electionId} history={history} action={action} tallySheetListRow={tallySheetListRow}
                    />
                });
            } else {
                return <TableCell align="center">{tallySheetListRow[column]}</TableCell>
            }
        })}
    </TableRow>

}

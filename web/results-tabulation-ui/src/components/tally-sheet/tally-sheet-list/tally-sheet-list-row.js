import React, {useEffect, useState} from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";

import TallySheetListRowAction, {TALLY_SHEET_LIST_ROW_ACTION} from "./tally-sheet-list-row-action";
import TextField from "@material-ui/core/TextField/TextField";
import {TALLY_SHEET_LIST_COLUMN} from "./index";


export default function TallySheetListRow(
    {
        history,
        electionId,
        tallySheetListRow,
        columns = [
            TALLY_SHEET_LIST_COLUMN,
            TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        actions = [
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VIEW,
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
            TALLY_SHEET_LIST_ROW_ACTION.TALLY_SHEET_LIST_ROW_ACTION_UNLOCK
        ]
    }
) {

    return <TableRow key={tallySheetListRow.tallySheetId}>
        {columns.map((column) => {
            if (column == TALLY_SHEET_LIST_COLUMN.TALLY_SHEET_LIST_COLUMN_ACTIONS) {
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



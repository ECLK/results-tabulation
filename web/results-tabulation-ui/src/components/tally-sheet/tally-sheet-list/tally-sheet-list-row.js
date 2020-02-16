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
import {fieldMatch} from "../../../utils";


export default function TallySheetListRow(
    {
        history,
        electionId,
        tallySheetListRow,
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

    const hasFilterMatch = () => {
        let _hasFilterMatch = true;
        for (let i = 0; i < columns.length; i++) {
            const column = columns[i];
            if (columnMetaMap[column] && columnMetaMap[column].filter && columnMetaMap[column].filter !== "") {
                if (_hasFilterMatch && !fieldMatch(tallySheetListRow[column], columnMetaMap[column].filter)) {
                    _hasFilterMatch = false;
                    break;
                }
            }
        }

        return _hasFilterMatch;
    };

    if (hasFilterMatch()) {
        return <TableRow key={tallySheetListRow.tallySheetId}>
            {columns.map((column) => {
                if (column == TALLY_SHEET_LIST_COLUMN_ACTIONS) {
                    return actions.map((action) => {
                        return <TallySheetListRowAction
                            electionId={electionId} history={history} action={action}
                            tallySheetListRow={tallySheetListRow}
                        />
                    });
                } else {
                    return <TableCell align="center">{tallySheetListRow[column]}</TableCell>
                }
            })}
        </TableRow>
    } else {
        return null;
    }


}

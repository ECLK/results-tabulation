import React, {useContext} from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY,
    TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../constants/TALLY_SHEET_ACTION";
import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS,
    TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_VALUE
} from "../constants/TALLY_SHEET_COLUMN";
import {fieldMatch} from "../../../utils";
import TallySheetActions from "../tally-sheet-actions";
import {TallySheetContext} from "../../../services/tally-sheet.provider";


export default function TallySheetListRow(
    {
        history,
        electionId,
        tallySheetId,
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
    // debugger;

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

    const tallySheetContext = useContext(TallySheetContext);
    let tallySheet = tallySheetContext.getTallySheetById(tallySheetId);
    tallySheet = appendColumnValuesToTallySheetRow(tallySheet);

    const hasFilterMatch = () => {
        let _hasFilterMatch = true;
        for (let i = 0; i < columns.length; i++) {
            const column = columns[i];
            if (columnMetaMap[column] && columnMetaMap[column].filter && columnMetaMap[column].filter !== "") {
                if (_hasFilterMatch && !fieldMatch(tallySheet[column], columnMetaMap[column].filter)) {
                    _hasFilterMatch = false;
                    break;
                }
            }
        }

        return _hasFilterMatch;
    };

    if (hasFilterMatch()) {
        return <TableRow key={tallySheet.tallySheetId}>
            {columns.map((column, columnIndex) => {
                let columnCellContent = null;
                if (column == TALLY_SHEET_LIST_COLUMN_ACTIONS) {
                    columnCellContent = <TallySheetActions
                        tallySheetId={tallySheet.tallySheetId}
                        electionId={electionId} history={history}
                    />
                } else {
                    columnCellContent = tallySheet[column];
                }

                return <TableCell key={columnIndex} align="center">{columnCellContent}</TableCell>
            })}
        </TableRow>
    } else {
        return null;
    }


}

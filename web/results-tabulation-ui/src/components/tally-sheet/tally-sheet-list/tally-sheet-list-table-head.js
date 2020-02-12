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
import TallySheetListTableBody from "./tally-sheet-list-table-body";


export default function TallySheetListTableHead(
    {
        columns = [
            TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        onColumnMetaChange = (columnMetaMap) => {
            console.log("=== onColumnMetaChange ", columnMetaMap)
        }
    }
) {
    const [columnMetaMap, setColumnMetaMap] = React.useState({});


    useEffect(() => {
        const columnMetaMap = {};
        columns.map((column) => {
            columnMetaMap[column] = {filter: "", label: TALLY_SHEET_LIST_COLUMN_LABEL[column]};
        });
        setColumnMetaMap(columnMetaMap);
    }, [columns]);

    // useEffect(() => {
    //     onColumnMetaChange(columnMetaMap);
    // }, [columnMetaMap]);

    const handleColumnFilterEnter = () => event => {
        console.log(`Pressed keyCode ${event.key}`);
        if (event.key === 'Enter') {
            onColumnMetaChange(columnMetaMap);
            event.preventDefault();
        }
    };

    const handleColumnFilter = column => event => {
        const {value} = event.target;
        setColumnMetaMap({
            ...columnMetaMap,
            [column]: {
                ...columnMetaMap[column],
                filter: value
            }
        });
    };

    const getColumnMeta = (column) => {
        if (columnMetaMap[column]) {
            return columnMetaMap[column];
        } else {
            return {filter: "", label: ""}
        }
    };


    return <TableHead>
        <TableRow>
            {columns.map((column, columnIndex) => {
                const columnMeta = getColumnMeta(column);

                return <TableCell align="center" key={columnIndex}>
                    <TextField
                        style={{width: "100%"}}
                        value={columnMeta.filter}
                        margin="dense"
                        variant="outlined"
                        placeholder={columnMeta.label}
                        onChange={handleColumnFilter(column)}
                        onKeyPress={handleColumnFilterEnter()}
                        inputProps={{
                            onKeyDown: handleColumnFilterEnter()
                        }}
                    />
                </TableCell>
            })}
        </TableRow>
        <TableRow>
            {columns.map((column, columnIndex) => {
                const columnMeta = getColumnMeta(column);

                return <TableCell align="center" key={columnIndex}>{columnMeta.label}</TableCell>
            })}
        </TableRow>
    </TableHead>
}

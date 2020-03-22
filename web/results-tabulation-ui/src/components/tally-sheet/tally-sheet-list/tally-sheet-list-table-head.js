import React, {useEffect} from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TextField from "@material-ui/core/TextField/TextField";
import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_LABEL, TALLY_SHEET_LIST_COLUMN_STATUS
} from "../constants/TALLY_SHEET_COLUMN";


export default function TallySheetListTableHead(
    {
        columns = [
            TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN_ACTIONS
        ],
        onColumnMetaChange = (columnMetaMap) => {
            // console.log("=== onColumnMetaChange ", columnMetaMap)
        }
    }
) {
    const [columnMetaMap, setColumnMetaMap] = React.useState({});


    useEffect(() => {
        const columnMetaMap = {};
        for (let columnIndex = 0; columnIndex < columns.length; columnIndex++) {
            const column = columns[columnIndex];
            columnMetaMap[column] = {filter: "", label: TALLY_SHEET_LIST_COLUMN_LABEL[column]};
        }

        setColumnMetaMap(columnMetaMap);
    }, [columns]);

    // useEffect(() => {
    //     onColumnMetaChange(columnMetaMap);
    // }, [columnMetaMap]);

    const handleColumnFilterEnter = () => event => {
        // console.log(`Pressed keyCode ${event.key}`);
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

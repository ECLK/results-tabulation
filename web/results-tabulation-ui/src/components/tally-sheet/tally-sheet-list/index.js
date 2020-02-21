import React, {useEffect, useState} from "react";
import {getTallySheet} from "../../../services/tabulation-api";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import {getTallySheetCodeStr} from "../../../utils/tallySheet";
import {
    PATH_ELECTION,
    PATH_ELECTION_BY_ID, PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
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
import {TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_STATUS} from "../constants/TALLY_SHEET_COLUMN";
import TallySheetListTableBody from "./tally-sheet-list-table-body";
import TallySheetListTableHead from "./tally-sheet-list-table-head";


export default function TallySheetList(
    {
        history,
        tallySheetCode,
        election,
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
    const {electionId, rootElectionId, rootElection} = election;
    const [columnMetaMap, setColumnMetaMap] = React.useState({});

    return <div className="page-content">
        <div>{rootElection.electionName}</div>
        <div>{getTallySheetCodeStr({tallySheetCode, election: election})}</div>
        <Table aria-label="simple table">
            <TallySheetListTableHead
                columns={columns}
                onColumnMetaChange={setColumnMetaMap}
            />
            <TallySheetListTableBody
                history={history}
                tallySheetCode={tallySheetCode}
                election={election}
                columns={columns}
                columnMetaMap={columnMetaMap}
                actions={actions}
            />
        </Table>
    </div>
}

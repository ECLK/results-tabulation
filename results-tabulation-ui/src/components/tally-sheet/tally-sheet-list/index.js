import React from "react";
import {getTallySheetCodeStr} from "../../../utils/tallySheet";
import Table from "@material-ui/core/Table";
import {TALLY_SHEET_LIST_COLUMN_ACTIONS, TALLY_SHEET_LIST_COLUMN_STATUS} from "../constants/TALLY_SHEET_COLUMN";
import TallySheetListTableBody from "./tally-sheet-list-table-body";
import TallySheetListTableHead from "./tally-sheet-list-table-head";

export default function TallySheetList(
    {
        history,
        tallySheetCode,
        voteType,
        partyId,
        election,
        columns = [
            TALLY_SHEET_LIST_COLUMN_STATUS,
            TALLY_SHEET_LIST_COLUMN_ACTIONS
        ]
    }
) {
    const {rootElection} = election;
    const [columnMetaMap, setColumnMetaMap] = React.useState({});

    return <div className="page-content">
        <div>{rootElection.electionName}</div>
        <div>{getTallySheetCodeStr({tallySheetCode, voteType})}</div>
        <Table aria-label="simple table">
            <TallySheetListTableHead
                columns={columns}
                onColumnMetaChange={setColumnMetaMap}
            />
            <TallySheetListTableBody
                history={history}
                tallySheetCode={tallySheetCode}
                voteType={voteType}
                partyId={partyId}
                election={election}
                columns={columns}
                columnMetaMap={columnMetaMap}
            />
        </Table>
    </div>
}

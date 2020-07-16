import React, {useContext, useEffect, useState} from "react";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Processing from "../../processing";
import TableBody from "@material-ui/core/TableBody";
import TallySheetListRow from "./tally-sheet-list-row";
import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS,
    TALLY_SHEET_LIST_COLUMN_STATUS
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
        columnMetaMap = {}
    }
) {
    const tallySheetContext = useContext(TallySheetContext);
    const {electionId} = election;
    const [tallySheetIds, setTallySheetIds] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        tallySheetContext.fetchTallySheetChunks({electionId, tallySheetCode, voteType}, (tallySheetIds) => {
            setTallySheetIds(prevState => {
                return [...prevState, ...tallySheetIds]
            });
        }).then(() => {
            setProcessing(false);
        }).catch((error) => {
            console.log(error.stack);
            setError(true);
            setProcessing(false);
        });
    }, []);

    const getTallySheetListJsx = function () {
        return tallySheetIds.map((tallySheetId, tallySheetIdIndex) => (<TallySheetListRow
            key={tallySheetIdIndex}
            tallySheetId={tallySheetId} history={history} electionId={electionId}
            columns={columns}
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
    } else if (!tallySheetIds || error) {
        tableBody = <TableRow>
            <TableCell colSpan={5} align="center">
                Tally sheet list cannot be accessed
            </TableCell>
        </TableRow>
    } else if (tallySheetIds) {
        if (tallySheetIds.length === 0) {
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

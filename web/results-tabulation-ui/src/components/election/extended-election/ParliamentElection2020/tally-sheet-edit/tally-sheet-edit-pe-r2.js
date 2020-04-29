import React, {useState} from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

import {isNumeric, processNumericValue} from "../../../../../utils";
import Processing from "../../../../processing";
import {useTallySheetEdit} from "../../../../tally-sheet/tally-sheet-edit";
import {
    TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2,
    TALLY_SHEET_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1,
    TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TALLY_SHEET_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT,
    TALLY_SHEET_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1
} from "../TALLY_SHEET_ROW_TYPE";

export default function TallySheetEdit_PE_R2({history, queryString, election, tallySheet, messages}) {

    const [tallySheetRows, setTallySheetRows] = useState({
        [TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED]: {
            templateRow: {}, map: {}
        }
    });

    const _forEachParty = (callback) => {
        const {parties} = election;
        for (let partyIndex = 0; partyIndex < parties.length; partyIndex++) {
            const party = parties[partyIndex];
            callback(party);
        }
    };

    const getTallySheetRow = (key, templateRowType) => {
        if (tallySheetRows[templateRowType] && tallySheetRows[templateRowType].map && tallySheetRows[templateRowType].map[key]) {
            return tallySheetRows[templateRowType].map[key];
        }

        return null
    };

    const setValue = (key, templateRowType, valuePropertyName = "numValue", value) => {
        setTallySheetRows((tallySheetRows) => {
            tallySheetRows = {...tallySheetRows};
            Object.assign(tallySheetRows[templateRowType].map[key], {[valuePropertyName]: processNumericValue(value)});

            return tallySheetRows;
        });
    };

    const getValue = (key, templateRowType, valuePropertyName = "numValue") => {
        const tallySheetRow = getTallySheetRow(key, templateRowType);
        if (tallySheetRow) {
            return tallySheetRow[valuePropertyName];
        }

        return 0;
    };

    const handleValueChange = (key, templateRowType, valuePropertyName = "numValue") => event => {
        const {value} = event.target;

        setValue(key, templateRowType, valuePropertyName, value);
    };


    const setTallySheetContent = async (tallySheetVersion) => {

        const _tallySheetRows = {...tallySheetRows};

        // Get the `templateRow` assigned to each type of tally sheet rows.
        tallySheet.template.rows.map(((templateRow) => {
            if (_tallySheetRows[templateRow.templateRowType]) {
                Object.assign(_tallySheetRows[templateRow.templateRowType].templateRow, templateRow)
            }
        }));

        // TODO append default values. For PE-R2, it could be assumed that the content always has valid data

        if (tallySheetVersion) {
            const {content} = tallySheetVersion;

            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];

                if (_tallySheetRows[contentRow.templateRowType]) {
                    try {
                        _tallySheetRows[contentRow.templateRowType].map[contentRow.partyId] = contentRow;
                    } catch (e) {
                        debugger;
                    }
                }
            }
        }

        setTallySheetRows(_tallySheetRows);


    };

    const validateTallySheetContent = () => {
        // TODO

        return true;
    };

    const getTallySheetRequestBody = () => {
        const content = [];

        [
            TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1,
            TALLY_SHEET_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1,
            TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2,
            TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED,
            TALLY_SHEET_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2,
            TALLY_SHEET_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED,
            TALLY_SHEET_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION,
            TALLY_SHEET_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT,
            TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED
        ].map((templateRowType) => {
            _forEachParty((party) => {
                const {partyId} = party;
                const tallySheetRow = getTallySheetRow(partyId, templateRowType);
                if (tallySheetRow) {
                    content.push(tallySheetRow);
                }
            });
        });

        return {
            content: content
        };
    };

    const {processing, processingLabel, saved, getActionsBar} = useTallySheetEdit({
        messages,
        history,
        election,
        tallySheet,
        setTallySheetContent,
        validateTallySheetContent,
        getTallySheetRequestBody
    });


    function getTallySheetEditForm() {
        return <div>
            TODO
            {getActionsBar()}
        </div>
    }

    return <Processing showProgress={processing} label={processingLabel}>
        {getTallySheetEditForm()}
    </Processing>;
}

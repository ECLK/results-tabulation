import React, {useState} from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';

import {isNumeric, processNumericValue} from "../../../../../utils";
import Processing from "../../../../processing";
import {useTallySheetEdit} from "../../../../tally-sheet/tally-sheet-edit";
import {
    TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE,
    TALLY_SHEET_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED,
    TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1,
    TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TALLY_SHEET_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT,
    TALLY_SHEET_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
} from "../TALLY_SHEET_ROW_TYPE";

export default function TallySheetEdit_PE_21({history, queryString, election, tallySheet, messages}) {

    const [tallySheetRows, setTallySheetRows] = useState({
        [TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE]: {
            templateRow: {}, map: {}
        },
        [TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE]: {
            templateRow: {}, map: {}
        }
    });
    const [allocatedSeatCountTotal, setAllocatedSeatCountTotal] = useState(0);

    const helperTextMap = {
        [TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED]: (partyId) => {
            const bonusSeatsAllocated = getValue(partyId, TALLY_SHEET_ROW_TYPE_BONUS_SEATS_ALLOCATED, "numValue");
            const bonusSeatsAllocatedDraft = getValue(partyId, TALLY_SHEET_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED, "numValue");

        },
        [TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2]: (partyId) => {
            const seatsAllocatedFromSecondRound = getValue(partyId, TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, "numValue");
            const seatsAllocatedFromSecondRoundDraft = getValue(partyId, TALLY_SHEET_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, "numValue");

        }
    };

    const getHelperText = (partyId, templateRowType) => {
        return helperTextMap[templateRowType](partyId);
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
            debugger;
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
        debugger;
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

            let seatIndex = 0;

            for (let i = 0; i < content.length; i++) {
                if (content[i].templateRowType !== TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED) {
                    continue;
                }

                let seatsAllocatedRow = content[i];
                const partyId = seatsAllocatedRow.partyId;
                const numberOfSeatsAllocated = seatsAllocatedRow.numValue;

                _tallySheetRows[TALLY_SHEET_ROW_TYPE_SEATS_ALLOCATED].map[partyId] = seatsAllocatedRow;

                const draftedElectedCandidateRows = content.filter((row) => {
                    return row.templateRowType === TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE && row.partyId === partyId
                }).sort((a, b) => {
                    return a.numValue > b.numValue ? 1 : a.numValue < b.numValue ? -1 : 0
                });

                debugger;
                for (let j = 0; j < numberOfSeatsAllocated; j++) {
                    let candidateId = null;
                    if (draftedElectedCandidateRows.length > j) {
                        candidateId = draftedElectedCandidateRows[j].candidateId
                    }

                    _tallySheetRows[TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE].map[seatIndex] = {candidateId, partyId};
                    _tallySheetRows[TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE].map[seatIndex] = {
                        ..._tallySheetRows[TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE].map[seatIndex]
                    };

                    seatIndex++;
                }
            }

            setAllocatedSeatCountTotal(seatIndex);
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
            TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE,
            TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE
        ].map((templateRowType) => {
            for (let seatIndex = 0; seatIndex < allocatedSeatCountTotal; seatIndex++) {
                const tallySheetRow = getTallySheetRow(seatIndex, templateRowType);
                if (tallySheetRow) {
                    content.push({
                        ...tallySheetRow,
                        ...tallySheetRows[templateRowType].templateRow
                    });
                } else {
                    break;
                }
            }
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

    const currencies = [
        {
            value: 'USD',
            label: '$',
        },
        {
            value: 'EUR',
            label: '€',
        },
        {
            value: 'BTC',
            label: '฿',
        },
        {
            value: 'JPY',
            label: '¥',
        },
    ];

    const [currency, setCurrency] = React.useState('EUR');

    const handleChange = (event) => {
        setCurrency(event.target.value);
    };


    function getTallySheetEditForm() {
        const {parties} = election;

        if (saved) {

            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Party</TableCell>
                        <TableCell align="center">Selected Candidate</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {(() => {
                        const rows = [];
                        for (let seatIndex = 0; seatIndex < allocatedSeatCountTotal; seatIndex++) {
                            const draftCandidateId = getValue(seatIndex, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE, "candidateId");
                            const partyId = getValue(seatIndex, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE, "partyId");
                            const candidateId = getValue(seatIndex, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE, "candidateId");

                            const party = election.partyMap[partyId];

                            rows.push(<TableRow key={partyId}>
                                <TableCell align="center">
                                    {party.partyName}
                                </TableCell>
                                <TableCell align="center">
                                    {candidateId}
                                </TableCell>
                            </TableRow>);
                        }

                        return rows;
                    })()}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>
                            {getActionsBar()}
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        } else if (!processing) {

            return <Table aria-label="simple table" size="medium">
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Party</TableCell>
                        <TableCell align="center">Selected Candidate</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {(() => {
                        const rows = [];
                        for (let seatIndex = 0; seatIndex < allocatedSeatCountTotal; seatIndex++) {
                            const draftCandidateId = getValue(seatIndex, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE, "candidateId");
                            const partyId = getValue(seatIndex, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE, "partyId");
                            const candidateId = getValue(seatIndex, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE, "candidateId");

                            const party = election.partyMap[partyId];

                            rows.push(<TableRow key={partyId}>
                                <TableCell align="center">
                                    {party.partyName}
                                </TableCell>
                                <TableCell align="center">
                                    {(() => {
                                        if (!candidateId) {
                                            return <small>Not available yet. Please check preference tally
                                                sheets.</small>
                                        } else {
                                            return <TextField
                                                required
                                                select
                                                variant="outlined"
                                                helperText={""}
                                                value={candidateId}
                                                margin="normal"
                                                onChange={handleValueChange(seatIndex, TALLY_SHEET_ROW_TYPE_ELECTED_CANDIDATE, "candidateId")}
                                                style={{
                                                    width: '200px'
                                                }}
                                            >
                                                {party.candidates.map(({candidateId, candidateName}) => (
                                                    <MenuItem key={candidateId} value={candidateId}>
                                                        {candidateName}
                                                    </MenuItem>
                                                ))}
                                            </TextField>
                                        }
                                    })()}
                                </TableCell>
                            </TableRow>);
                        }

                        return rows;
                    })()}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>
                            {getActionsBar()}
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        } else {
            return null;
        }
    }

    return <Processing showProgress={processing} label={processingLabel}>
        {getTallySheetEditForm()}
    </Processing>;
}

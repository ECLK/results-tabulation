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

export default function TallySheetEdit_PE_22({history, election, tallySheet, messages}) {
    const [invalidVoteCategoryCountRows, setInvalidVoteCategoryCountRows] = useState([]);
    const [parties, setParties] = useState([]);
    const [partyWiseInvalidVoteCategoryCountRows, setPartyWiseInvalidVoteCategoryCountRows] = useState([]);
    const [partyWiseRejectedVoteCountRows, setPartyWiseRejectedVoteCountRows] = useState([]);
    const [rejectedVoteCountRow, setRejectedVoteCountRow] = useState({"numValue": 0});

    const setTallySheetContent = (tallySheetVersion) => {
        let _invalidVoteCategoryCountRowTemplate = {};
        let _partyWiseRejectedVoteCountRows = [];
        let _rejectedVoteCountRow = {"numValue": 0};

        tallySheet.template.rows.forEach(templateRow => {
            if (templateRow.templateRowType === "PARTY_WISE_INVALID_VOTE_COUNT") {
                _invalidVoteCategoryCountRowTemplate = templateRow;
            }
        });

        const _invalidVoteCategoryCountRows = [];
        election.invalidVoteCategories.filter(invalidVoteCategory => {
            return invalidVoteCategory.invalidVoteCategoryType === "PARTY_SPECIFIC"
        }).sort((a, b) => {
            return a.invalidVoteCategoryId - b.invalidVoteCategoryId;
        }).forEach(invalidVoteCategory => {
            _invalidVoteCategoryCountRows.push({
                ...tallySheet.area,
                ...invalidVoteCategory,
                ..._invalidVoteCategoryCountRowTemplate
            });
        });

        const _partyWiseInvalidVoteCategoryCountRows = [];
        const _parties = [];
        election.parties
            .sort((a, b) => {
                return a.partyId - b.partyId
            })
            .forEach(party => {
                _invalidVoteCategoryCountRows.forEach(invalidVoteCategoryCountRow => {
                    _partyWiseInvalidVoteCategoryCountRows.push({
                        ...invalidVoteCategoryCountRow,
                        partyId: party.partyId,
                        partyName: party.partyName,
                        numValue: 0
                    });
                })

                _partyWiseRejectedVoteCountRows.push({
                    partyId: party.partyId,
                    partyName: party.partyName,
                    numValue: 0
                })

                _parties.push(party);
            });

        if (tallySheetVersion) {
            const {content} = tallySheetVersion;
            const _partyToRejectedVoteCount = {};
            for (let i = 0; i < content.length; i++) {
                const contentRow = content[i];
                if (contentRow.templateRowType === "PARTY_WISE_INVALID_VOTE_COUNT") {
                    const {partyId, invalidVoteCategoryId} = contentRow;
                    const matchingInvalidVoteCountRow = _partyWiseInvalidVoteCategoryCountRows.filter(invalidVoteCategoryCountRow => {
                        return invalidVoteCategoryCountRow.partyId === partyId && invalidVoteCategoryCountRow.invalidVoteCategoryId === invalidVoteCategoryId
                    })[0];
                    Object.assign(matchingInvalidVoteCountRow, contentRow);
                    _partyToRejectedVoteCount[partyId] = (_partyToRejectedVoteCount[partyId] === undefined)
                        ? matchingInvalidVoteCountRow.numValue
                        : _partyToRejectedVoteCount[partyId] + matchingInvalidVoteCountRow.numValue;
                }
            }

            let _totalRejectedVoteCount = 0

            _partyWiseRejectedVoteCountRows.forEach(rejectedVoteCountRow => {
                const rejectedVoteCount = _partyToRejectedVoteCount[rejectedVoteCountRow.partyId];
                ;
                rejectedVoteCountRow.numValue = rejectedVoteCount;
                _totalRejectedVoteCount += rejectedVoteCount;
            });

            _rejectedVoteCountRow.numValue = _totalRejectedVoteCount;
        }

        setInvalidVoteCategoryCountRows(_invalidVoteCategoryCountRows);
        setParties(_parties);
        setPartyWiseInvalidVoteCategoryCountRows(_partyWiseInvalidVoteCategoryCountRows);
        setPartyWiseRejectedVoteCountRows(_partyWiseRejectedVoteCountRows);
        setRejectedVoteCountRow(_rejectedVoteCountRow);
    };

    function getPartyInvalidVoteCategoryCountRows(partyId) {
        return partyWiseInvalidVoteCategoryCountRows.filter(invalidVoteCategoryCountRow => invalidVoteCategoryCountRow.partyId === partyId);
    }

    function getPartRejectedVoteCountRow(partyId) {
        return partyWiseRejectedVoteCountRows.filter(rejectedVoteCountRow => rejectedVoteCountRow.partyId === partyId);
    }

    function calculatePartyWiseRejectedVoteCount(partyId) {
        let _totalRejectedVoteCount = 0;
        partyWiseInvalidVoteCategoryCountRows
            .filter(invalidVoteCategoryCountRow => invalidVoteCategoryCountRow.partyId === partyId)
            .forEach(invalidVoteCategoryCountRow => {
                _totalRejectedVoteCount += invalidVoteCategoryCountRow.numValue;
            });
        return _totalRejectedVoteCount;
    }

    function calculateTotalRejectedVoteCount() {
        let _totalRejectedVoteCount = 0;
        parties.forEach(party => {
            _totalRejectedVoteCount += calculatePartyWiseRejectedVoteCount(party.partyId);
        })
        return _totalRejectedVoteCount;
    }

    const validateTallySheetContent = () => {
        for (let i = 0; i < partyWiseInvalidVoteCategoryCountRows.length; i++) {
            if (!(isNumeric(partyWiseInvalidVoteCategoryCountRows[i].numValue))) {
                return false;
            }
        }

        let _totalRejectedVoteCount = 0;

        for (let j = 0; j < partyWiseRejectedVoteCountRows.length; j++) {
            const _partyWiseRejectedVoteCountRow = partyWiseRejectedVoteCountRows[j];
            const _rejectedVoteCount = calculatePartyWiseRejectedVoteCount(_partyWiseRejectedVoteCountRow.partyId);
            if (!(isNumeric(_partyWiseRejectedVoteCountRow.numValue)) || _rejectedVoteCount !== _partyWiseRejectedVoteCountRow.numValue) {
                return false;
            }
            _totalRejectedVoteCount += _rejectedVoteCount;
        }

        return (isNumeric(rejectedVoteCountRow.numValue) && (rejectedVoteCountRow.numValue === _totalRejectedVoteCount))
    };

    const getTallySheetRequestBody = () => {

        return {
            content: [
                ...partyWiseInvalidVoteCategoryCountRows
            ]
        }
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

    const handlePartyWiseInvalidVoteCountChange = key => event => {
        const [partyId, invalidVoteCategoryId] = key.split("-").map(value => Number(value));
        const {value} = event.target;

        setPartyWiseInvalidVoteCategoryCountRows((partyWiseInvalidVoteCategoryCountRows) => {
            const _partyWiseInvalidVoteCategoryCountRows = [...partyWiseInvalidVoteCategoryCountRows];
            _partyWiseInvalidVoteCategoryCountRows
                .filter(invalidVoteCategoryCountRow =>
                    invalidVoteCategoryCountRow.partyId === partyId && invalidVoteCategoryCountRow.invalidVoteCategoryId === invalidVoteCategoryId
                )[0].numValue = processNumericValue(value);
            return _partyWiseInvalidVoteCategoryCountRows;
        });
    }

    const handlePartyWiseRejectedVoteCountChange = partyId => event => {
        const {value} = event.target;
        setPartyWiseRejectedVoteCountRows(partyWiseRejectedVoteCountRows => {
            const _partyWiseRejectedVoteCountRows = [...partyWiseRejectedVoteCountRows];
            _partyWiseRejectedVoteCountRows
                .filter(rejectedVoteCountRow => rejectedVoteCountRow.partyId === partyId)[0].numValue = processNumericValue(value);
            return _partyWiseRejectedVoteCountRows;
        });
    }

    const handleRejectedVoteCountChange = () => event => {
        const {value} = event.target;
        setRejectedVoteCountRow((rejectedVoteCountRow) => {
            return {
                ...rejectedVoteCountRow,
                numValue: processNumericValue(value)
            }
        });
    }


    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="left">Name of the Party/Independent Group</TableCell>
                        {
                            invalidVoteCategoryCountRows.map((invalidVoteCategoryCountRow, invalidVoteCategoryCountRowIndex) => {
                                const {categoryDescription} = invalidVoteCategoryCountRow;
                                return <TableCell align="right"
                                                  key={invalidVoteCategoryCountRowIndex}>{categoryDescription}</TableCell>
                            })
                        }
                        <TableCell align="right">Total</TableCell>
                    </TableRow>
                </TableHead>

                <TableBody>
                    {
                        parties.map((party, partyIndex) => {
                            const {partyId, partyName} = party;
                            const rejectedVoteCountRow = getPartRejectedVoteCountRow(partyId)[0]
                            return <TableRow key={partyIndex}>
                                <TableCell align="left">{partyName}</TableCell>
                                {
                                    getPartyInvalidVoteCategoryCountRows(partyId).map(invalidVoteCategoryCountRow => {
                                        const {invalidVoteCategoryId, numValue} = invalidVoteCategoryCountRow;
                                        const key = partyId + "-" + invalidVoteCategoryId;
                                        return <TableCell align="right" key={key}>{numValue}</TableCell>
                                    })
                                }
                                <TableCell align="right" key={partyId}>{rejectedVoteCountRow.numValue}</TableCell>
                            </TableRow>
                        })
                    }
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={4}>Total rejected vote count</TableCell>
                        <TableCell align="right" colSpan={5}>{rejectedVoteCountRow.numValue}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={5}>
                            {getActionsBar()}
                        </TableCell>
                    </TableRow>

                </TableFooter>

            </Table>
        } else if (!processing) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="left">Name of the Party/Independent Group</TableCell>
                        {
                            invalidVoteCategoryCountRows.map((invalidVoteCategoryCountRow, invalidVoteCategoryCountRowIndex) => {
                                const {categoryDescription} = invalidVoteCategoryCountRow;
                                return <TableCell align="right"
                                                  key={invalidVoteCategoryCountRowIndex}>{categoryDescription}</TableCell>
                            })
                        }
                        <TableCell align="right">Total</TableCell>
                    </TableRow>
                </TableHead>

                <TableBody>
                    {
                        parties.map((party, partyIndex) => {
                            const {partyId, partyName} = party;
                            const rejectedVoteCountRow = getPartRejectedVoteCountRow(partyId)[0]
                            return <TableRow key={partyIndex}>
                                <TableCell align="left">{partyName}</TableCell>
                                {
                                    getPartyInvalidVoteCategoryCountRows(partyId).map(invalidVoteCategoryCountRow => {
                                        const {invalidVoteCategoryId, numValue} = invalidVoteCategoryCountRow;
                                        const key = partyId + "-" + invalidVoteCategoryId;
                                        return <TableCell align="right" key={key}>
                                            <TextField
                                                required
                                                variant="outlined"
                                                error={!isNumeric(numValue)}
                                                helperText={!isNumeric(numValue) ? "Only numeric values are valid" : ''}
                                                value={numValue}
                                                margin="normal"
                                                onChange={handlePartyWiseInvalidVoteCountChange(key)}
                                                inputProps={{
                                                    style: {
                                                        height: '10px'
                                                    },
                                                }}
                                            />
                                        </TableCell>
                                    })
                                }
                                <TableCell align="right" key={partyId}>
                                    <TextField
                                        required
                                        variant="outlined"
                                        error={calculatePartyWiseRejectedVoteCount(partyId) !== rejectedVoteCountRow.numValue}
                                        helperText={calculatePartyWiseRejectedVoteCount(partyId) !== rejectedVoteCountRow.numValue ? "Party invalid vote count mismatch!" : ''}
                                        value={rejectedVoteCountRow.numValue}
                                        margin="normal"
                                        onChange={handlePartyWiseRejectedVoteCountChange(partyId)}
                                        inputProps={{
                                            style: {
                                                height: '10px'
                                            },
                                        }}
                                    />
                                </TableCell>
                            </TableRow>
                        })
                    }
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={4}>Total rejected vote count</TableCell>
                        <TableCell align="right" colSpan={5}><TextField
                            required
                            error={calculateTotalRejectedVoteCount() !== rejectedVoteCountRow.numValue}
                            helperText={calculateTotalRejectedVoteCount() !== rejectedVoteCountRow.numValue ? 'Total invalid vote count mismatch!' : ' '}
                            value={rejectedVoteCountRow.numValue}
                            margin="normal"
                            onChange={handleRejectedVoteCountChange()}
                        /></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={5}>
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
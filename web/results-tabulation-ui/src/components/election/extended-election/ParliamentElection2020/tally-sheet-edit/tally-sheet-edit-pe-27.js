import React, {useState} from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

import Button from '@material-ui/core/Button';
import {isNumeric, processNumericValue} from "../../../../../utils";
import Processing from "../../../../processing";
import {useTallySheetEdit} from "../../../../tally-sheet/tally-sheet-edit";

export default function TallySheetEdit_PE_27({history, queryString, election, tallySheet, messages}) {
    const [partWiseVoteCountRows, setPartWiseVoteCountRows] = useState([]);
    const [rejectedVoteCountRow, setRejectedVoteCountRow] = useState({"numValue": 0});
    const [validVoteCountRow, setValidVoteCountRow] = useState({"numValue": 0});
    const [voteCountRow, setVoteCountRow] = useState({"numValue": 0});


    const setTallySheetContent = (tallySheetVersion) => {
        let _partyWiseVoteCountTemplateRow = {};
        let _rejectedVoteCountTemplateRow = {};

        tallySheet.template.rows.map(((templateRow) => {
            if (templateRow.templateRowType === "PARTY_WISE_VOTE") {
                _partyWiseVoteCountTemplateRow = templateRow;
            } else if (templateRow.templateRowType === "REJECTED_VOTE") {
                _rejectedVoteCountTemplateRow = templateRow;
            }
        }));

        let _partWiseVoteCountRowsMap = {};
        let _partWiseVoteCountRows = [];
        let _rejectedVoteCountRow = {..._rejectedVoteCountTemplateRow, numValue: 0};
        let _validVoteCountRow = {numValue: 0};
        let _voteCountRow = {numValue: 0};

        election.rootElection.parties.map(party => {
            const _partWiseVoteCountRow = {
                ...party,
                ..._partyWiseVoteCountTemplateRow,
                numValue: 0,
                strValue: ""
            };
            _partWiseVoteCountRowsMap[party.partyId] = _partWiseVoteCountRow;
            _partWiseVoteCountRows.push(_partWiseVoteCountRow);
        });


        if (tallySheetVersion) {
            const {content} = tallySheetVersion;
            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                if (contentRow.templateRowType === "PARTY_WISE_VOTE") {
                    _partWiseVoteCountRowsMap[contentRow.partyId].numValue = contentRow.numValue;
                    _partWiseVoteCountRowsMap[contentRow.partyId].strValue = contentRow.strValue;
                    _partWiseVoteCountRowsMap[contentRow.partyId].templateRowId = contentRow.templateRowId;
                    _partWiseVoteCountRowsMap[contentRow.partyId].templateRowType = contentRow.templateRowType;
                    _validVoteCountRow.numValue += contentRow.numValue;
                } else if (contentRow.templateRowType === "REJECTED_VOTE") {
                    _rejectedVoteCountRow.numValue = contentRow.numValue;
                    _rejectedVoteCountRow.templateRowId = contentRow.templateRowId;
                    _rejectedVoteCountRow.templateRowType = contentRow.templateRowType;
                }
            }

            _voteCountRow.numValue = _validVoteCountRow.numValue + _rejectedVoteCountRow.numValue;
        }

        setPartWiseVoteCountRows(_partWiseVoteCountRows);
        setRejectedVoteCountRow(_rejectedVoteCountRow);
        setValidVoteCountRow(_validVoteCountRow);
        setVoteCountRow(_voteCountRow);
    };

    const validateTallySheetContent = () => {
        for (let i = 0; i < partWiseVoteCountRows.length; i++) {
            if (!isNumeric(partWiseVoteCountRows[i]["numValue"])) {
                return false;
            }
        }

        return (isNumeric(rejectedVoteCountRow.numValue) &&
            calculateTotalVoteCount() === voteCountRow.numValue &&
            calculateTotalValidVoteCount() === validVoteCountRow.numValue
        )
    };

    const getTallySheetRequestBody = () => {

        return {
            content: [
                ...partWiseVoteCountRows,
                rejectedVoteCountRow
            ]

            //     tallySheet.template.rows.map(((templateRow) => {
            //     const contentRow = {
            //         templateRowId: templateRow.templateRowId,
            //         rows: []
            //     };
            //
            //     if (templateRow.templateRowType === "PARTY_WISE_VOTE") {
            //         contentRow.rows = partWiseVoteCountRows
            //     } else if (templateRow.templateRowType === "REJECTED_VOTE") {
            //         contentRow.rows = [rejectedVoteCountRow];
            //     }
            //
            //     return contentRow
            // }))
        }
    };

    const {processing, processingLabel, saved, handleClickNext, handleClickSubmit, handleClickBackToEdit} = useTallySheetEdit({
        messages,
        history,
        election,
        tallySheet,
        setTallySheetContent,
        validateTallySheetContent,
        getTallySheetRequestBody
    });


    const handleValidVoteCountChange = partWiseVoteCountRowIndex => event => {
        const {value} = event.target;
        setPartWiseVoteCountRows((partWiseVoteCountRows) => {
            const _partWiseVoteCountRows = [...partWiseVoteCountRows];

            _partWiseVoteCountRows[partWiseVoteCountRowIndex] = {
                ..._partWiseVoteCountRows[partWiseVoteCountRowIndex],
                numValue: processNumericValue(value)
            };

            return _partWiseVoteCountRows
        });
    };

    const handleValidVoteCountInWordsChange = partWiseVoteCountRowIndex => event => {
        const {value} = event.target;
        setPartWiseVoteCountRows((partWiseVoteCountRows) => {
            const _partWiseVoteCountRows = [...partWiseVoteCountRows];

            _partWiseVoteCountRows[partWiseVoteCountRowIndex] = {
                ..._partWiseVoteCountRows[partWiseVoteCountRowIndex],
                strValue: value
            };

            return _partWiseVoteCountRows
        });
    };


    function calculateTotalValidVoteCount() {
        let total = 0;
        for (let i = 0; i < partWiseVoteCountRows.length; i++) {
            total += parseInt(partWiseVoteCountRows[i]["numValue"])
        }

        return total;
    }

    function calculateTotalVoteCount() {
        return calculateTotalValidVoteCount() + parseInt(rejectedVoteCountRow.numValue);
    }


    const handleTotalValidVoteCountChange = () => event => {
        const {value} = event.target;
        setValidVoteCountRow((validVoteCountRow) => {
            return {
                ...validVoteCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    const handleRejectedVoteCountChange = () => event => {
        const {value} = event.target;
        setRejectedVoteCountRow((rejectedVoteCountRow) => {
            return {
                ...rejectedVoteCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    const handleTotalVoteCountChange = () => event => {
        const {value} = event.target;
        setVoteCountRow((voteCountRow) => {
            return {
                ...voteCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Party Name</TableCell>
                        <TableCell align="center">Party Symbol</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {partWiseVoteCountRows.map((partWiseVoteCountRow) => {
                        const {partyId, partyName, partySymbol, strValue, numValue} = partWiseVoteCountRow;
                        return <TableRow key={partyId}>
                            <TableCell align="center">{partyName}</TableCell>
                            <TableCell align="center">{partySymbol}</TableCell>
                            <TableCell align="center">{strValue}</TableCell>
                            <TableCell align="right">{numValue}</TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total valid vote count</TableCell>
                        <TableCell align="right">{calculateTotalValidVoteCount()}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total rejected vote count</TableCell>
                        <TableCell align="right">{rejectedVoteCountRow.numValue}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">{calculateTotalVoteCount()}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={4}>
                            <div className="page-bottom-fixed-action-bar">
                                <Button
                                    variant="contained" color="default" onClick={handleClickBackToEdit()}
                                    disabled={processing}
                                >
                                    Edit
                                </Button>
                                <Button
                                    variant="contained" color="primary" onClick={handleClickSubmit()}
                                    disabled={processing}
                                >
                                    Submit
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>

                </TableFooter>

            </Table>
        } else if (!processing) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Party Name</TableCell>
                        <TableCell align="center">Party Symbol</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {partWiseVoteCountRows.map((partWiseVoteCountRow, partWiseVoteCountRowIndex) => {
                        const {partyId, partyName, partySymbol, strValue, numValue} = partWiseVoteCountRow;
                        console.log("==== partWiseVoteCountRow : ", partWiseVoteCountRow);
                        return <TableRow key={partyId}>
                            <TableCell align="center">{partyName}</TableCell>
                            <TableCell align="center">{partySymbol}</TableCell>
                            <TableCell align="center">
                                <TextField
                                    required
                                    variant="outlined"
                                    className={"data-entry-edit-count-in-words-input"}
                                    value={strValue}
                                    margin="normal"
                                    onChange={handleValidVoteCountInWordsChange(partWiseVoteCountRowIndex)}
                                    inputProps={{
                                        style: {
                                            height: '10px'
                                        },
                                    }}
                                />
                            </TableCell>
                            <TableCell align="center">
                                <TextField
                                    required
                                    variant="outlined"
                                    error={!isNumeric(numValue)}
                                    helperText={!isNumeric(numValue) ? "Only numeric values are valid" : ''}
                                    value={numValue}
                                    margin="normal"
                                    onChange={handleValidVoteCountChange(partWiseVoteCountRowIndex)}
                                    inputProps={{
                                        style: {
                                            height: '10px'
                                        },
                                    }}
                                />
                            </TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total valid vote count</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={calculateTotalValidVoteCount() !== validVoteCountRow.numValue}
                                helperText={calculateTotalValidVoteCount() !== validVoteCountRow.numValue ? 'Total valid vote count mismatch!' : ' '}
                                value={validVoteCountRow.numValue}
                                margin="normal"
                                onChange={handleTotalValidVoteCountChange()}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total rejected vote count</TableCell>
                        <TableCell align="right"><TextField
                            required
                            error={!isNumeric(rejectedVoteCountRow.numValue)}
                            helperText={!isNumeric(rejectedVoteCountRow.numValue) ? "Only numeric values are valid" : ''}
                            value={rejectedVoteCountRow.numValue}
                            margin="normal"
                            onChange={handleRejectedVoteCountChange()}
                        /></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={calculateTotalVoteCount() !== voteCountRow.numValue}
                                helperText={calculateTotalVoteCount() !== voteCountRow.numValue ? 'Total vote count mismatch!' : ' '}
                                value={voteCountRow.numValue}
                                margin="normal"
                                onChange={handleTotalVoteCountChange()}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={4}>
                            <div className="page-bottom-fixed-action-bar">
                                <Button
                                    variant="contained" color="default" onClick={handleClickNext()}
                                    disabled={processing}
                                >
                                    Save & Next
                                </Button>
                            </div>
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
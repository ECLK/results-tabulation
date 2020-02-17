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

export default function TallySheetEdit_PE_4({history, queryString, election, tallySheet, messages}) {
    const [candidateWiseFirstPreferenceCountRows, setCandidateWiseFirstPreferenceCountRows] = useState([]);
    const [rejectedFirstPreferenceCountRow, setRejectedFirstPreferenceCountRow] = useState({"numValue": 0});
    const [validFirstPreferenceCountRow, setValidFirstPreferenceCountRow] = useState({"numValue": 0});
    const [firstPreferenceCountRow, setFirstPreferenceCountRow] = useState({"numValue": 0});


    const setTallySheetContent = (tallySheetVersion) => {
        let _candidateWiseFirstPreferenceCountTemplateRow = {};
        let _rejectedFirstPreferenceCountTemplateRow = {};

        tallySheet.template.rows.map(((templateRow) => {
            if (templateRow.templateRowType === "CANDIDATE_FIRST_PREFERENCE") {
                _candidateWiseFirstPreferenceCountTemplateRow = templateRow;
            } else if (templateRow.templateRowType === "REJECTED_VOTE") {
                _rejectedFirstPreferenceCountTemplateRow = templateRow;
            }
        }));

        let _candidateWiseFirstPreferenceCountRowsMap = {};
        let _candidateWiseFirstPreferenceCountRows = [];
        let _rejectedFirstPreferenceCountRow = {..._rejectedFirstPreferenceCountTemplateRow, numValue: 0};
        let _validFirstPreferenceCountRow = {numValue: 0};
        let _firstPreferenceCountRow = {numValue: 0};

        debugger;
        election.rootElection.partyMap[tallySheet.metaDataMap["partyId"]].candidates.map(candidate => {
            const _candidateWiseFirstPreferenceCountRow = {
                ...candidate,
                ..._candidateWiseFirstPreferenceCountTemplateRow,
                numValue: 0,
                strValue: ""
            };
            _candidateWiseFirstPreferenceCountRowsMap[candidate.candidateId] = _candidateWiseFirstPreferenceCountRow;
            _candidateWiseFirstPreferenceCountRows.push(_candidateWiseFirstPreferenceCountRow);
        });


        if (tallySheetVersion) {
            const {content} = tallySheetVersion;
            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                if (contentRow.templateRowType === "CANDIDATE_FIRST_PREFERENCE") {
                    Object.assign(_candidateWiseFirstPreferenceCountRowsMap[contentRow.candidateId], contentRow);
                    _validFirstPreferenceCountRow.numValue += contentRow.numValue;
                } else if (contentRow.templateRowType === "REJECTED_VOTE") {
                    Object.assign(_rejectedFirstPreferenceCountRow, contentRow);
                }
            }

            _firstPreferenceCountRow.numValue = _validFirstPreferenceCountRow.numValue + _rejectedFirstPreferenceCountRow.numValue;
        }

        setCandidateWiseFirstPreferenceCountRows(_candidateWiseFirstPreferenceCountRows);
        setRejectedFirstPreferenceCountRow(_rejectedFirstPreferenceCountRow);
        setValidFirstPreferenceCountRow(_validFirstPreferenceCountRow);
        setFirstPreferenceCountRow(_firstPreferenceCountRow);
    };

    const validateTallySheetContent = () => {
        for (let i = 0; i < candidateWiseFirstPreferenceCountRows.length; i++) {
            if (!isNumeric(candidateWiseFirstPreferenceCountRows[i]["numValue"])) {
                return false;
            }
        }

        return (isNumeric(rejectedFirstPreferenceCountRow.numValue) &&
            calculateTotalFirstPreferenceCount() === firstPreferenceCountRow.numValue &&
            calculateTotalValidFirstPreferenceCount() === validFirstPreferenceCountRow.numValue
        )
    };

    const getTallySheetRequestBody = () => {

        return {
            content: [
                ...candidateWiseFirstPreferenceCountRows,
                // rejectedFirstPreferenceCountRow TODO
            ]
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


    const handleValidFirstPreferenceCountChange = candidateWiseFirstPreferenceCountRowIndex => event => {
        const {value} = event.target;
        setCandidateWiseFirstPreferenceCountRows((candidateWiseFirstPreferenceCountRows) => {
            const _candidateWiseFirstPreferenceCountRows = [...candidateWiseFirstPreferenceCountRows];

            _candidateWiseFirstPreferenceCountRows[candidateWiseFirstPreferenceCountRowIndex] = {
                ..._candidateWiseFirstPreferenceCountRows[candidateWiseFirstPreferenceCountRowIndex],
                numValue: processNumericValue(value)
            };

            return _candidateWiseFirstPreferenceCountRows
        });
    };

    const handleValidFirstPreferenceCountInWordsChange = candidateWiseFirstPreferenceCountRowIndex => event => {
        const {value} = event.target;
        setCandidateWiseFirstPreferenceCountRows((candidateWiseFirstPreferenceCountRows) => {
            const _candidateWiseFirstPreferenceCountRows = [...candidateWiseFirstPreferenceCountRows];

            _candidateWiseFirstPreferenceCountRows[candidateWiseFirstPreferenceCountRowIndex] = {
                ..._candidateWiseFirstPreferenceCountRows[candidateWiseFirstPreferenceCountRowIndex],
                strValue: value
            };

            return _candidateWiseFirstPreferenceCountRows
        });
    };


    function calculateTotalValidFirstPreferenceCount() {
        let total = 0;
        for (let i = 0; i < candidateWiseFirstPreferenceCountRows.length; i++) {
            total += parseInt(candidateWiseFirstPreferenceCountRows[i]["numValue"])
        }

        return total;
    }

    function calculateTotalFirstPreferenceCount() {
        return calculateTotalValidFirstPreferenceCount() + parseInt(rejectedFirstPreferenceCountRow.numValue);
    }


    const handleTotalValidFirstPreferenceCountChange = () => event => {
        const {value} = event.target;
        setValidFirstPreferenceCountRow((validFirstPreferenceCountRow) => {
            return {
                ...validFirstPreferenceCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    const handleRejectedFirstPreferenceCountChange = () => event => {
        const {value} = event.target;
        setRejectedFirstPreferenceCountRow((rejectedFirstPreferenceCountRow) => {
            return {
                ...rejectedFirstPreferenceCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    const handleTotalFirstPreferenceCountChange = () => event => {
        const {value} = event.target;
        setFirstPreferenceCountRow((firstPreferenceCountRow) => {
            return {
                ...firstPreferenceCountRow,
                numValue: processNumericValue(value)
            }
        });
    };

    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Candidate Name</TableCell>
                        <TableCell align="center">Candidate Number</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {candidateWiseFirstPreferenceCountRows.map((candidateWiseFirstPreferenceCountRow) => {
                        const {candidateId, candidateName, strValue, numValue} = candidateWiseFirstPreferenceCountRow;
                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center"></TableCell>
                            <TableCell align="center">{strValue}</TableCell>
                            <TableCell align="right">{numValue}</TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total valid vote count</TableCell>
                        <TableCell align="right">{calculateTotalValidFirstPreferenceCount()}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total rejected vote count</TableCell>
                        <TableCell align="right">{rejectedFirstPreferenceCountRow.numValue}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">{calculateTotalFirstPreferenceCount()}</TableCell>
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
                        <TableCell align="center">Candidate Name</TableCell>
                        <TableCell align="center">Candidate Number</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {candidateWiseFirstPreferenceCountRows.map((candidateWiseFirstPreferenceCountRow, candidateWiseFirstPreferenceCountRowIndex) => {
                        const {candidateId, candidateName, strValue, numValue} = candidateWiseFirstPreferenceCountRow;
                        console.log("==== candidateWiseFirstPreferenceCountRow : ", candidateWiseFirstPreferenceCountRow);
                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center"></TableCell>
                            <TableCell align="center">
                                <TextField
                                    required
                                    variant="outlined"
                                    className={"data-entry-edit-count-in-words-input"}
                                    value={strValue}
                                    margin="normal"
                                    onChange={handleValidFirstPreferenceCountInWordsChange(candidateWiseFirstPreferenceCountRowIndex)}
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
                                    onChange={handleValidFirstPreferenceCountChange(candidateWiseFirstPreferenceCountRowIndex)}
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
                                error={calculateTotalValidFirstPreferenceCount() !== validFirstPreferenceCountRow.numValue}
                                helperText={calculateTotalValidFirstPreferenceCount() !== validFirstPreferenceCountRow.numValue ? 'Total valid vote count mismatch!' : ' '}
                                value={validFirstPreferenceCountRow.numValue}
                                margin="normal"
                                onChange={handleTotalValidFirstPreferenceCountChange()}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total rejected vote count</TableCell>
                        <TableCell align="right"><TextField
                            required
                            error={!isNumeric(rejectedFirstPreferenceCountRow.numValue)}
                            helperText={!isNumeric(rejectedFirstPreferenceCountRow.numValue) ? "Only numeric values are valid" : ''}
                            value={rejectedFirstPreferenceCountRow.numValue}
                            margin="normal"
                            onChange={handleRejectedFirstPreferenceCountChange()}
                        /></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={calculateTotalFirstPreferenceCount() !== firstPreferenceCountRow.numValue}
                                helperText={calculateTotalFirstPreferenceCount() !== firstPreferenceCountRow.numValue ? 'Total vote count mismatch!' : ' '}
                                value={firstPreferenceCountRow.numValue}
                                margin="normal"
                                onChange={handleTotalFirstPreferenceCountChange()}
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
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

export default function TallySheetEdit_PE_4({history, queryString, election, tallySheet}) {
    const [candidateWiseFirstPreferenceCountRows, setCandidateWiseFirstPreferenceCountRows] = useState([]);
    const [firstPreferenceCountRow, setFirstPreferenceCountRow] = useState({"numValue": 0});


    const setTallySheetContent = (tallySheetVersion) => {
        let _candidateWiseFirstPreferenceCountTemplateRow = {};

        tallySheet.template.rows.map(((templateRow) => {
            if (templateRow.templateRowType === "CANDIDATE_FIRST_PREFERENCE") {
                _candidateWiseFirstPreferenceCountTemplateRow = templateRow;
            }
        }));

        let _candidateWiseFirstPreferenceCountRowsMap = {};
        let _candidateWiseFirstPreferenceCountRows = [];
        let _validFirstPreferenceCountRow = {numValue: 0};
        let _firstPreferenceCountRow = {numValue: 0};

        election.partyMap[tallySheet.metaDataMap["partyId"]].candidates.map(candidate => {
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
                }
            }

            _firstPreferenceCountRow.numValue = _validFirstPreferenceCountRow.numValue;
        }

        setCandidateWiseFirstPreferenceCountRows(_candidateWiseFirstPreferenceCountRows);
        setFirstPreferenceCountRow(_firstPreferenceCountRow);
    };

    const validateTallySheetContent = () => {
        for (let i = 0; i < candidateWiseFirstPreferenceCountRows.length; i++) {
            if (!isNumeric(candidateWiseFirstPreferenceCountRows[i]["numValue"])) {
                return false;
            }
        }

        return true;
    };

    const getTallySheetRequestBody = () => {

        return {
            content: [
                ...candidateWiseFirstPreferenceCountRows,
            ]
        }
    };

    const {processing, processingLabel, saved, getActionsBar} = useTallySheetEdit({
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
                        const {candidateId, candidateName, candidateNumber, strValue, numValue} = candidateWiseFirstPreferenceCountRow;
                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center">{candidateNumber}</TableCell>
                            <TableCell align="center">{strValue}</TableCell>
                            <TableCell align="right">{numValue}</TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={4}>
                            {getActionsBar()}
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
                        <TableCell align="center">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {candidateWiseFirstPreferenceCountRows.map((candidateWiseFirstPreferenceCountRow, candidateWiseFirstPreferenceCountRowIndex) => {
                        const {candidateId, candidateName, candidateNumber, strValue, numValue} = candidateWiseFirstPreferenceCountRow;

                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center">{candidateNumber}</TableCell>
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
                                        maxLength: 100
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
                        <TableCell align="right" colSpan={4}>
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

import React, { useState } from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

import Button from '@material-ui/core/Button';
import { isNumeric, processNumericValue } from "../../../../../utils";
import Processing from "../../../../processing";
import { useTallySheetEdit } from "../../../../tally-sheet/tally-sheet-edit";
import { convertColorToString } from "material-ui/utils/colorManipulator";

export default function TallySheetEdit_PE_39({ history, election, tallySheet, messages }) {
    const [rejectionReasonWiseVoteCountRows, setRejectionReasonWiseVoteCountRows] = useState([]);
    const [rejectedVoteCountRow, setRejectedVoteCountRow] = useState({ "numValue": 0 });

    const setTallySheetContent = (tallySheetVersion) => {
        let _rejectionReasonWiseVoteCountTemplateRow = {};
        let _rejectedVoteCountTemplateRow = {};

        tallySheet.template.rows.map(templateRow => {
            if (templateRow.templateRowType === "NUMBER_OF_VOTES_REJECTED_AGAINST_GROUNDS_FOR_REJECTION") {
                _rejectionReasonWiseVoteCountTemplateRow = templateRow;
            } else if (templateRow.templateRowType === "REJECTED_VOTE") {
                _rejectedVoteCountTemplateRow = templateRow;
            }
        });

        const _rejectionReasonWiseVoteCountRows = [];
        const _rejectionReasonWiseVoteCountRowsMap = {};
        election.invalidVoteCategories.map(invalidVoteCategory => {
            const _rejectionReasonWiseVoteCountRow = {
                ...tallySheet.area,
                ...invalidVoteCategory,
                ..._rejectionReasonWiseVoteCountTemplateRow,
                numValue: 0
            };
            _rejectionReasonWiseVoteCountRowsMap[invalidVoteCategory.invalidVoteCategoryId] = _rejectionReasonWiseVoteCountRow;
            _rejectionReasonWiseVoteCountRows.push(_rejectionReasonWiseVoteCountRow);
        });

        const _rejectedVoteCountRow = {
            ...tallySheet.area,
            ..._rejectedVoteCountTemplateRow,
            numValue: 0
        };

        if (tallySheetVersion) {
            const { content } = tallySheetVersion;
            for (let i = 0; i < content.length; i++) {
                const contentRow = content[i];

                if (contentRow.templateRowType === "NUMBER_OF_VOTES_REJECTED_AGAINST_GROUNDS_FOR_REJECTION") {
                    Object.assign(_rejectionReasonWiseVoteCountRowsMap[contentRow.invalidVoteCategoryId], contentRow);
                } else if (contentRow.templateRowType === "REJECTED_VOTE") {
                    Object.assign(_rejectedVoteCountRow, contentRow);
                }
            }
        }


        setRejectionReasonWiseVoteCountRows(_rejectionReasonWiseVoteCountRows);
        setRejectedVoteCountRow(_rejectedVoteCountRow);
    };

    function calculateTotalRejectedVoteCount() {
        let totalRejectedVotes = 0;
        for (let i = 0; i < rejectionReasonWiseVoteCountRows.length; i++) {
            totalRejectedVotes += rejectionReasonWiseVoteCountRows[i].numValue;
        }
        return totalRejectedVotes;
    }

    const validateTallySheetContent = () => {
        for (let i = 0; i < rejectionReasonWiseVoteCountRows.length; i++) {
            if (!(isNumeric(rejectionReasonWiseVoteCountRows[i].numValue))) {
                return false;
            }
        }

        return  (isNumeric(rejectedVoteCountRow.numValue) && (calculateTotalRejectedVoteCount() === rejectedVoteCountRow.numValue));
    };

    const getTallySheetRequestBody = () => {

        return {
            content: [
                ...rejectionReasonWiseVoteCountRows,
                rejectedVoteCountRow
            ]
        }
    };

    const { processing, processingLabel, saved, handleClickNext, handleClickSubmit, handleClickBackToEdit } = useTallySheetEdit({
        messages,
        history,
        election,
        tallySheet,
        setTallySheetContent,
        validateTallySheetContent,
        getTallySheetRequestBody
    });

    const handleRejectionReasonWiseVoteCountChange = rejectionReasonWiseVoteCountRowIndex => event => {
        const { value } = event.target;
        setRejectionReasonWiseVoteCountRows(rejectionReasonWiseVoteCountRows => {
            const _rejectionReasonWiseVoteCountRows = [...rejectionReasonWiseVoteCountRows];

            _rejectionReasonWiseVoteCountRows[rejectionReasonWiseVoteCountRowIndex] = {
                ..._rejectionReasonWiseVoteCountRows[rejectionReasonWiseVoteCountRowIndex],
                numValue: processNumericValue(value)
            }

            return _rejectionReasonWiseVoteCountRows;
        });
    }

    const handleRejectedVoteCountChange = () => event => {
        const { value } = event.target;
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
                        <TableCell align="left">Grounds for Rejection</TableCell>
                        <TableCell align="right">Number of Ballot Papers Rejected</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rejectionReasonWiseVoteCountRows.map(rejectionReasonWiseVoteCountRow => {
                        const { invalidVoteCategoryId, categoryDescription, numValue } = rejectionReasonWiseVoteCountRow;
                        return <TableRow key={invalidVoteCategoryId}>
                            <TableCell align="left">{categoryDescription}</TableCell>
                            <TableCell align="right">{numValue}</TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right">Total rejected vote count</TableCell>
                        <TableCell align="right">{rejectedVoteCountRow.numValue}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
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
                        <TableCell align="left">Grounds for Rejection</TableCell>
                        <TableCell align="right">Number of Ballot Papers Rejected</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rejectionReasonWiseVoteCountRows.map((rejectionReasonWiseVoteCountRow, rejectionReasonWiseVoteCountRowIndex) => {
                        const { invalidVoteCategoryId, categoryDescription, numValue } = rejectionReasonWiseVoteCountRow;
                        return <TableRow key={invalidVoteCategoryId}>
                            <TableCell align="left">{categoryDescription}</TableCell>
                            <TableCell align="right">
                                <TextField
                                    required
                                    variant="outlined"
                                    error={!isNumeric(numValue)}
                                    helperText={!isNumeric(numValue) ? "Only numeric values are valid" : ''}
                                    value={numValue}
                                    margin="normal"
                                    onChange={handleRejectionReasonWiseVoteCountChange(rejectionReasonWiseVoteCountRowIndex)}
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
                        <TableCell align="right">Total rejected vote count</TableCell>
                        <TableCell align="right"><TextField
                            required
                            error={calculateTotalRejectedVoteCount() !== rejectedVoteCountRow.numValue}
                            helperText={calculateTotalRejectedVoteCount() !== rejectedVoteCountRow.numValue ? 'Total valid vote count mismatch!' : ' '}
                            value={rejectedVoteCountRow.numValue}
                            margin="normal"
                            onChange={handleRejectedVoteCountChange()}
                        /></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
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
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

export default function TallySheetEdit_PRE_41({history, election, tallySheet, messages}) {
    const [candidateWiseCounts, setCandidateWiseCounts] = useState({});
    const [rejectedVoteCount, setRejectedVoteCount] = useState(0);
    const [totalValidVoteCount, setTotalValidVoteCount] = useState(0);
    const [totalVoteCount, setTotalVoteCount] = useState(0);

    const _forEachCandidate = (callback) => {
        const {parties} = election;
        for (let partyIndex = 0; partyIndex < parties.length; partyIndex++) {
            const party = parties[partyIndex];
            const {candidates} = party;
            for (let candidateIndex = 0; candidateIndex < candidates.length; candidateIndex++) {
                const candidate = candidates[candidateIndex];
                callback(candidate, party);
            }
        }
    };

    const _mapEachCandidate = (callback) => {
        const _mapList = [];
        _forEachCandidate(() => {
            _mapList.push(_forEachCandidate);
        });

        return _mapList
    };

    const setTallySheetContent = (tallySheetVersion) => {
        const latestCandidateWiseCounts = {};
        const {parties} = election;
        _forEachCandidate((candidate) => {
            latestCandidateWiseCounts[candidate.candidateId] = {
                candidateId: candidate.candidateId,
                validVoteCount: 0,
                validVoteCountInWords: ""
            };
        });

        if (tallySheetVersion) {
            const {content} = tallySheetVersion;
            let validTotal = 0;
            let rejectedVoteCount = 0;
            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                const {templateRowType} = contentRow;
                if (templateRowType === "CANDIDATE_FIRST_PREFERENCE") {
                    latestCandidateWiseCounts[contentRow.candidateId] = {
                        candidateId: contentRow.candidateId,
                        validVoteCount: contentRow.numValue,
                        validVoteCountInWords: contentRow.strValue
                    };
                    validTotal += contentRow.numValue;
                } else if (templateRowType === "REJECTED_VOTE") {
                    rejectedVoteCount = contentRow.numValue;
                    setRejectedVoteCount(contentRow.numValue);
                }

            }
            setTotalValidVoteCount(validTotal);
            setTotalVoteCount((validTotal + rejectedVoteCount));
        }

        setCandidateWiseCounts(latestCandidateWiseCounts);
    };

    const validateTallySheetContent = () => {
        for (let key in candidateWiseCounts) {
            if (!isNumeric(candidateWiseCounts[key]["validVoteCount"])) {
                return false;
            }
        }

        return (isNumeric(rejectedVoteCount) &&
            calculateTotalVoteCount() === totalVoteCount &&
            calculateTotalValidVoteCount() === totalValidVoteCount
        )
    };

    const getTallySheetRequestBody = () => {
        const rejected_vote_rows = [{"numValue": rejectedVoteCount}];
        const candidate_first_preference_rows = [];

        _forEachCandidate((candidate, party) => {
            const {candidateId} = candidate;
            const {partyId} = party;
            const {validVoteCount, validVoteCountInWords} = candidateWiseCounts[candidateId];
            candidate_first_preference_rows.push({
                partyId: partyId,
                candidateId: candidateId,
                numValue: validVoteCount,
                strValue: validVoteCountInWords
            })
        });

        return {
            content: tallySheet.template.rows.map(((templateRow) => {
                const contentRow = {
                    templateRowId: templateRow.templateRowId,
                    rows: []
                };

                if (templateRow.templateRowType === "CANDIDATE_FIRST_PREFERENCE") {
                    contentRow.rows = candidate_first_preference_rows
                } else if (templateRow.templateRowType === "REJECTED_VOTE") {
                    contentRow.rows = rejected_vote_rows;
                }

                return contentRow
            }))
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


    const handleValidVoteCountChange = candidateId => event => {
        setCandidateWiseCounts({
            ...candidateWiseCounts,
            [candidateId]: {
                ...candidateWiseCounts[candidateId],
                validVoteCount: processNumericValue(event.target.value)
            }
        })
    };

    const handleValidVoteCountInWordsChange = candidateId => event => {
        setCandidateWiseCounts({
            ...candidateWiseCounts,
            [candidateId]: {
                ...candidateWiseCounts[candidateId],
                validVoteCountInWords: event.target.value
            }
        })
    };


    function calculateTotalValidVoteCount() {
        let total = 0;
        for (let key in candidateWiseCounts) {
            total += parseInt(candidateWiseCounts[key]["validVoteCount"])
        }

        return total;
    }

    function calculateTotalVoteCount() {
        return calculateTotalValidVoteCount() + parseInt(rejectedVoteCount);
    }


    const handleTotalValidVoteCountChange = () => event => {
        setTotalValidVoteCount(processNumericValue(event.target.value));
    };

    const handleRejectedVoteCountChange = () => event => {
        setRejectedVoteCount(processNumericValue(event.target.value));
    };

    const handleTotalVoteCountChange = () => event => {
        setTotalVoteCount(processNumericValue(event.target.value));
    };

    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Candidate Name</TableCell>
                        <TableCell align="center">Party Symbol</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {_mapEachCandidate((candidate, party) => {
                        const {candidateId, candidateName} = candidate;
                        const {partySymbol} = party;
                        const candidateWiseCount = candidateWiseCounts[candidateId];
                        const {validVoteCount, validVoteCountInWords} = candidateWiseCount;
                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center">{partySymbol}</TableCell>
                            <TableCell align="center">{validVoteCountInWords}</TableCell>
                            <TableCell align="right">{validVoteCount}</TableCell>
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
                        <TableCell align="right">{rejectedVoteCount}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">{calculateTotalVoteCount()}</TableCell>
                    </TableRow>
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
                        <TableCell align="center">Party Symbol</TableCell>
                        <TableCell align="center">Count in words</TableCell>
                        <TableCell align="right">Count in figures</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {_mapEachCandidate((candidate, party) => {
                        const {candidateId, candidateName} = candidate;
                        const {partySymbol} = party;
                        const candidateWiseCount = candidateWiseCounts[candidateId];
                        const {validVoteCount, validVoteCountInWords} = candidateWiseCount;
                        return <TableRow key={candidateId}>
                            <TableCell align="center">{candidateName}</TableCell>
                            <TableCell align="center">{partySymbol}</TableCell>
                            <TableCell align="center">
                                <TextField
                                    required
                                    variant="outlined"
                                    className={"data-entry-edit-count-in-words-input"}
                                    value={validVoteCountInWords}
                                    margin="normal"
                                    onChange={handleValidVoteCountInWordsChange(candidateId)}
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
                                    error={!isNumeric(validVoteCount)}
                                    helperText={!isNumeric(validVoteCount) ? "Only numeric values are valid" : ''}
                                    value={validVoteCount}
                                    margin="normal"
                                    onChange={handleValidVoteCountChange(candidateId)}
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
                                error={calculateTotalValidVoteCount() !== totalValidVoteCount}
                                helperText={calculateTotalValidVoteCount() !== totalValidVoteCount ? 'Total valid vote count mismatch!' : ' '}
                                value={totalValidVoteCount}
                                margin="normal"
                                onChange={handleTotalValidVoteCountChange()}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total rejected vote count</TableCell>
                        <TableCell align="right"><TextField
                            required
                            error={!isNumeric(rejectedVoteCount)}
                            helperText={!isNumeric(rejectedVoteCount) ? "Only numeric values are valid" : ''}
                            value={rejectedVoteCount}
                            margin="normal"
                            onChange={handleRejectedVoteCountChange()}
                        /></TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>Total vote count</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={calculateTotalVoteCount() !== totalVoteCount}
                                helperText={calculateTotalVoteCount() !== totalVoteCount ? 'Total vote count mismatch!' : ' '}
                                value={totalVoteCount}
                                margin="normal"
                                onChange={handleTotalVoteCountChange()}
                            />
                        </TableCell>
                    </TableRow>
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

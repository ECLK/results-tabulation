import React, {useState} from "react";
import {MESSAGES_EN} from "../../../../../locale/messages_en";
import {MESSAGE_TYPES} from "../../../../../services/messages.provider";
import {PATH_ELECTION_TALLY_SHEET_LIST} from "../../../../../App";
import {getErrorMessage, isNumeric, processNumericValue} from "../../../../../utils";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TextField from "@material-ui/core/TextField";
import Processing from "../../../../processing";
import {useTallySheetEdit} from "../../../../tally-sheet/tally-sheet-edit";

export default function TallySheetEdit_PRE_34_CO({history, queryString, election, tallySheet, messages}) {
    const {tallySheetCode} = tallySheet;
    const {electionId, voteType} = election;
    const [candidateIds, setCandidateIds] = useState([]);
    const [candidateWiseCounts, setCandidateWiseCounts] = useState({});
    const [summary, setSummary] = useState([]);

    const setTallySheetContent = (tallySheetVersion) => {
        const qualifiedParties = getQualifiedParties();
        const candidateIds = [];

        if (qualifiedParties.length === 0) {
            messages.push({
                messageTitle: "Error",
                messageBody: MESSAGES_EN.error_preferences_not_enabled_yet,
                messageType: MESSAGE_TYPES.ERROR
            });
            history.push(PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode, voteType));
        }

        if (tallySheetVersion) {
            const latestCandidateWiseCounts = {};
            const {content} = tallySheetVersion;
            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                let preferenceNo = "";
                let candidate = latestCandidateWiseCounts[contentRow.candidateId];
                let total = candidate == undefined ? 0 : candidate.totalCount;
                if (total === undefined) {
                    total = 0;
                }
                if (contentRow.preferenceNumber === 2) {
                    preferenceNo = "secondPreferenceCount"
                    candidateIds.push(contentRow.candidateId);
                } else if (contentRow.preferenceNumber === 3) {
                    preferenceNo = "thirdPreferenceCount"
                }
                latestCandidateWiseCounts[contentRow.candidateId] = {
                    ...latestCandidateWiseCounts[contentRow.candidateId],
                    candidateId: contentRow.candidateId,
                    candidateName: contentRow.candidateName,
                    [preferenceNo]: contentRow.preferenceCount,
                    totalCount: total + contentRow.preferenceCount
                };
            }

            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                if (contentRow.templateRowType === "CANDIDATE_SECOND_PREFERENCE") {
                    latestCandidateWiseCounts[contentRow.candidateId] = {
                        ...latestCandidateWiseCounts[contentRow.candidateId],
                        candidateId: contentRow.candidateId,
                        candidateName: contentRow.candidateName,
                        secondPreferenceCount: contentRow.numValue
                    };
                } else if (contentRow.templateRowType === "CANDIDATE_THIRD_PREFERENCE") {
                    latestCandidateWiseCounts[contentRow.candidateId] = {
                        ...latestCandidateWiseCounts[contentRow.candidateId],
                        candidateId: contentRow.candidateId,
                        candidateName: contentRow.candidateName,
                        thirdPreferenceCount: contentRow.numValue
                    };
                }

            }

            setCandidateWiseCounts(latestCandidateWiseCounts);
            setSummary({
                ballotPapersNotCounted: tallySheetVersion.summary.ballotPapersNotCounted,
                remainingBallotPapers: tallySheetVersion.summary.remainingBallotPapers,
                total: tallySheetVersion.summary.ballotPapersNotCounted + tallySheetVersion.summary.remainingBallotPapers
            });
            setCandidateIds(candidateIds);
        } else {
            const initialCandidateWiseCounts = {};
            election.parties.map(party => {
                party.candidates.map(candidate => {
                    if (candidate.qualifiedForPreferences) {
                        initialCandidateWiseCounts[candidate.candidateId] = {
                            candidateId: candidate.candidateId,
                            candidateName: candidate.candidateName,
                            secondPreferenceCount: 0,
                            thirdPreferenceCount: 0,
                            totalCount: 0
                        };
                        candidateIds.push(candidate.candidateId);
                    }
                });
            });
            setCandidateWiseCounts(initialCandidateWiseCounts);
            setSummary({
                ballotPapersNotCounted: 0,
                remainingBallotPapers: 0,
                total: 0
            });
            setCandidateIds(candidateIds);
        }
    };

    const validateTallySheetContent = () => {
        for (let key in candidateWiseCounts) {
            let secondPreference = candidateWiseCounts[key]["secondPreferenceCount"];
            let thirdPreference = candidateWiseCounts[key]["thirdPreferenceCount"];
            let totalCount = candidateWiseCounts[key]["totalCount"];

            if (!isNumeric(secondPreference)) {
                return false;
            }
            if (!isNumeric(thirdPreference)) {
                return false;
            }
            if (!isNumeric(totalCount)) {
                return false;
            }
            if (totalCount !== secondPreference + thirdPreference) {
                return false;
            }
        }

        return (summary.ballotPapersNotCounted + summary.remainingBallotPapers === summary.total)
    };

    const getTallySheetRequestBody = () => {
        const content = [];
        election.parties.map(party => {
            party.candidates.map(candidate => {
                const {candidateId} = candidate;
                if (candidateWiseCounts[candidateId] !== undefined) {
                    const {secondPreferenceCount, thirdPreferenceCount} = candidateWiseCounts[candidateId];
                    content.push({
                        candidateId: candidateId,
                        preferenceNumber: 2,
                        preferenceCount: secondPreferenceCount
                    })
                    content.push({
                        candidateId: candidateId,
                        preferenceNumber: 3,
                        preferenceCount: thirdPreferenceCount
                    })
                }
            })
        });

        return {
            content: content,
            summary: summary
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


    function getQualifiedParties() {
        const qualifiedParties = election.parties.filter(party => {
            for (let i = 0; i < party.candidates.length; i++) {
                let candidate = party.candidates[i];
                if (candidate.qualifiedForPreferences) {
                    return true;
                }
            }

            return false;
        });

        return qualifiedParties
    }

    const handleCountChange = (candidateId, preference) => event => {
        setCandidateWiseCounts({
            ...candidateWiseCounts,
            [candidateId]: {
                ...candidateWiseCounts[candidateId],
                [preference]: processNumericValue(event.target.value)
            }
        })
    };

    const handleSummaryChange = (key) => event => {
        setSummary({
            ...summary,
            [key]: processNumericValue(event.target.value)
        })
    };

    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableBody>
                    <TableRow>
                        {candidateIds.map(candidateId => {
                            const candidate = candidateWiseCounts[candidateId];
                            return <TableCell key={candidateId}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell colSpan={3} align="center">Candidate
                                                - {candidate.candidateName}</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell align="center">Total No of 2nd Preferences</TableCell>
                                            <TableCell align="center">Total No of 3rd Preferences</TableCell>
                                            <TableCell align="center">Total</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        <TableRow>
                                            <TableCell
                                                align="center">{candidate.secondPreferenceCount}</TableCell>
                                            <TableCell
                                                align="center">{candidate.thirdPreferenceCount}</TableCell>
                                            <TableCell
                                                align="center">{candidate.totalCount}</TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </TableCell>
                        })}
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[3] Ballot Papers Not Counted Section 58(2)</TableCell>
                        <TableCell align="right">{summary.ballotPapersNotCounted}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[4] Remaining Ballot Papers</TableCell>
                        <TableCell align="right">{summary.remainingBallotPapers}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[5] Total [3] + [4]</TableCell>
                        <TableCell align="right">{summary.total}</TableCell>
                    </TableRow>
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={6}>
                            {getActionsBar()}
                        </TableCell>
                    </TableRow>

                </TableFooter>

            </Table>
        } else if (!processing) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableBody>
                    <TableRow>
                        {candidateIds.map(candidateId => {
                            const candidate = candidateWiseCounts[candidateId];
                            return <TableCell key={candidateId}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell colSpan={3} align="center">Candidate
                                                - {candidate.candidateName}</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell align="center">Total No of 2nd Preferences</TableCell>
                                            <TableCell align="center">Total No of 3rd Preferences</TableCell>
                                            <TableCell align="center">Total</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        <TableRow>
                                            <TableCell align="center">
                                                <TextField
                                                    required
                                                    error={!isNumeric(candidate.secondPreferenceCount)}
                                                    helperText={!isNumeric(candidate.secondPreferenceCount) ? "Only numeric values are valid" : ''}
                                                    className={"data-entry-edit-count-input"}
                                                    value={candidate.secondPreferenceCount}
                                                    margin="normal"
                                                    onChange={handleCountChange(candidate.candidateId, "secondPreferenceCount")}
                                                />
                                            </TableCell>
                                            <TableCell align="center">
                                                <TextField
                                                    required
                                                    error={!isNumeric(candidate.thirdPreferenceCount)}
                                                    helperText={!isNumeric(candidate.thirdPreferenceCount) ? "Only numeric values are valid" : ''}
                                                    className={"data-entry-edit-count-input"}
                                                    value={candidate.thirdPreferenceCount}
                                                    margin="normal"
                                                    onChange={handleCountChange(candidate.candidateId, "thirdPreferenceCount")}
                                                />
                                            </TableCell>
                                            <TableCell align="center">
                                                <TextField
                                                    required
                                                    error={candidate.totalCount !== candidate.secondPreferenceCount + candidate.thirdPreferenceCount}
                                                    helperText={candidate.totalCount !== candidate.secondPreferenceCount + candidate.thirdPreferenceCount ? "Total is incorrect" : ''}
                                                    className={"data-entry-edit-count-input"}
                                                    value={candidate.totalCount}
                                                    margin="normal"
                                                    onChange={handleCountChange(candidate.candidateId, "totalCount")}
                                                />
                                            </TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </TableCell>
                        })}
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[3] Ballot Papers Not Counted Section 58(2)</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={!isNumeric(summary.ballotPapersNotCounted)}
                                helperText={!isNumeric(summary.ballotPapersNotCounted) ? "Only numeric values are valid" : ''}
                                className={"data-entry-edit-count-input"}
                                value={summary.ballotPapersNotCounted}
                                margin="normal"
                                onChange={handleSummaryChange("ballotPapersNotCounted")}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[4] Remaining Ballot Papers</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={!isNumeric(summary.remainingBallotPapers)}
                                helperText={!isNumeric(summary.remainingBallotPapers) ? "Only numeric values are valid" : ''}
                                className={"data-entry-edit-count-input"}
                                value={summary.remainingBallotPapers}
                                margin="normal"
                                onChange={handleSummaryChange("remainingBallotPapers")}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={1}>[5] Total [3] + [4]</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={summary.total !== summary.ballotPapersNotCounted + summary.remainingBallotPapers}
                                helperText={summary.total !== summary.ballotPapersNotCounted + summary.remainingBallotPapers ? "Total is incorrect" : ''}
                                className={"data-entry-edit-count-input"}
                                value={summary.total}
                                margin="normal"
                                onChange={handleSummaryChange("total")}
                            />
                        </TableCell>
                    </TableRow>
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={6}>
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

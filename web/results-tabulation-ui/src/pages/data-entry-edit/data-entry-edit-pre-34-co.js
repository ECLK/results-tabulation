import React, {useState} from "react";
import {isNumeric, processNumericValue} from "../../utils";
import {MESSAGE_TYPES} from "../../services/messages.provider";
import {PATH_ELECTION_DATA_ENTRY} from "../../App";
import Processing from "../../components/processing";
import Error from "../../components/error";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

import Button from '@material-ui/core/Button';
import {MESSAGES_EN} from "../../locale/messages_en";
import {useTallySheetEdit} from "./index";

export default function DataEntryEdit_PRE_34_CO({history, queryString, election, tallySheet, messages}) {
    const {tallySheetId, tallySheetCode} = tallySheet;
    const {electionId} = election;

    const [candidateIds, setCandidateIds] = useState([]);
    const [candidateWiseCounts, setCandidateWiseCounts] = useState({});
    // const [processing, setProcessing] = useState(true);
    // const [tallySheetVersion, setTallySheetVersion] = useState(null);
    // const [processingLabel, setProcessingLabel] = useState("Loading");
    // const [saved, setSaved] = useState(false);
    const [summary, setSummary] = useState([]);


    const setTallySheetContent = (tallySheetVersion) => {
        const subElectionId = tallySheet.electionId;
        const qualifiedParties = getQualifiedParties();

        if (qualifiedParties.length === 0) {
            messages.push("Error", MESSAGES_EN.error_preferences_not_enabled_yet, MESSAGE_TYPES.ERROR);
            // setTimeout(() => {
            history.push(PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId));
            //}, 5000);
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

            setCandidateWiseCounts(latestCandidateWiseCounts);
            setSummary({
                ballotPapersNotCounted: tallySheetVersion.summary.ballotPapersNotCounted,
                remainingBallotPapers: tallySheetVersion.summary.remainingBallotPapers,
                total: tallySheetVersion.summary.ballotPapersNotCounted + tallySheetVersion.summary.remainingBallotPapers
            });
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

    const {processing, processingLabel, saved, handleClickNext, handleClickSubmit, handleClickBackToEdit} = useTallySheetEdit({
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


    //
    // useEffect(() => {
    //     const subElectionId = tallySheet.electionId;
    //     const qualifiedParties = getQualifiedParties();
    //
    //     if (qualifiedParties.length === 0) {
    //         messages.push("Error", MESSAGES_EN.error_preferences_not_enabled_yet, MESSAGE_TYPES.ERROR);
    //         setTimeout(() => {
    //             history.push(PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId));
    //         }, 5000);
    //     } else if (tallySheet.latestVersionId) {
    //         getTallySheetVersionById(tallySheetId, tallySheetCode, tallySheet.latestVersionId).then((tallySheetVersion) => {
    //             const latestCandidateWiseCounts = {};
    //             const {content} = tallySheetVersion;
    //             for (let i = 0; i < content.length; i++) {
    //                 let contentRow = content[i];
    //                 let preferenceNo = "";
    //                 let candidate = latestCandidateWiseCounts[contentRow.candidateId];
    //                 let total = candidate == undefined ? 0 : candidate.totalCount;
    //                 if (total === undefined) {
    //                     total = 0;
    //                 }
    //                 if (contentRow.preferenceNumber === 2) {
    //                     preferenceNo = "secondPreferenceCount"
    //                     candidateIds.push(contentRow.candidateId);
    //                 } else if (contentRow.preferenceNumber === 3) {
    //                     preferenceNo = "thirdPreferenceCount"
    //                 }
    //                 latestCandidateWiseCounts[contentRow.candidateId] = {
    //                     ...latestCandidateWiseCounts[contentRow.candidateId],
    //                     candidateId: contentRow.candidateId,
    //                     candidateName: contentRow.candidateName,
    //                     [preferenceNo]: contentRow.preferenceCount,
    //                     totalCount: total + contentRow.preferenceCount
    //                 };
    //             }
    //             console.log("latest", candidateIds);
    //             console.log("latest", latestCandidateWiseCounts);
    //             setCandidateWiseCounts(latestCandidateWiseCounts);
    //             setSummary({
    //                 ballotPapersNotCounted: tallySheetVersion.summary.ballotPapersNotCounted,
    //                 remainingBallotPapers: tallySheetVersion.summary.remainingBallotPapers,
    //                 total: tallySheetVersion.summary.ballotPapersNotCounted + tallySheetVersion.summary.remainingBallotPapers
    //             });
    //         }).catch((error) => {
    //             console.log("error:", error);
    //             messages.push("Error", MESSAGES_EN.error_tallysheet_not_reachable, MESSAGE_TYPES.ERROR);
    //         })
    //     } else {
    //         const initialCandidateWiseCounts = {};
    //         election.parties.map(party => {
    //             party.candidates.map(candidate => {
    //                 if (candidate.qualifiedForPreferences) {
    //                     initialCandidateWiseCounts[candidate.candidateId] = {
    //                         candidateId: candidate.candidateId,
    //                         candidateName: candidate.candidateName,
    //                         secondPreferenceCount: 0,
    //                         thirdPreferenceCount: 0,
    //                         totalCount: 0
    //                     };
    //                     candidateIds.push(candidate.candidateId);
    //                 }
    //             });
    //         });
    //         setCandidateWiseCounts(initialCandidateWiseCounts);
    //         setSummary({
    //             ballotPapersNotCounted: 0,
    //             remainingBallotPapers: 0,
    //             total: 0
    //         });
    //     }
    // }, []);

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

    // const getTallySheetSaveRequestBody = () => {
    //     const content = [];
    //     election.parties.map(party => {
    //         party.candidates.map(candidate => {
    //             const {candidateId} = candidate;
    //             if (candidateWiseCounts[candidateId] !== undefined) {
    //                 const {secondPreferenceCount, thirdPreferenceCount} = candidateWiseCounts[candidateId];
    //                 content.push({
    //                     candidateId: candidateId,
    //                     preferenceNumber: 2,
    //                     preferenceCount: secondPreferenceCount
    //                 })
    //                 content.push({
    //                     candidateId: candidateId,
    //                     preferenceNumber: 3,
    //                     preferenceCount: thirdPreferenceCount
    //                 })
    //             }
    //         })
    //     });
    //
    //     return {
    //         content: content,
    //         summary: summary
    //     }
    // };

    // const handleClickNext = (saved = true) => async (event) => {
    //     console.log(validateAllValues());
    //     if (validateAllValues()) {
    //         setSaved(saved)
    //         setProcessing(true);
    //         setProcessingLabel("Saving");
    //         try {
    //             const body = getTallySheetSaveRequestBody();
    //             const tallySheetVersion = await saveTallySheetVersion(tallySheetId, tallySheetCode, body);
    //
    //             setTallySheetVersion(tallySheetVersion);
    //         } catch (e) {
    //             console.log(e);
    //             messages.push("Error", MESSAGES_EN.error_tallysheet_save, MESSAGE_TYPES.ERROR);
    //         }
    //         setProcessing(false);
    //     } else {
    //         messages.push("Error", MESSAGES_EN.error_input, MESSAGE_TYPES.ERROR)
    //     }
    // };
    //
    // const handleClickSubmit = () => async (event) => {
    //     setProcessing(true);
    //     setProcessingLabel("Submitting");
    //     try {
    //         const {tallySheetVersionId} = tallySheetVersion;
    //         const tallySheet = await submitTallySheet(tallySheetId, tallySheetVersionId);
    //
    //         messages.push("Success", MESSAGES_EN.success_pre41_submit, MESSAGE_TYPES.SUCCESS);
    //         setTimeout(() => {
    //             const subElectionId = tallySheet.electionId;
    //             history.push(PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId));
    //         }, 1000)
    //     } catch (e) {
    //         messages.push("Error", MESSAGES_EN.error_tallysheet_submit, MESSAGE_TYPES.ERROR);
    //     }
    //
    //     setProcessing(false);
    // };
    //
    // function validateAllValues() {
    //     for (let key in candidateWiseCounts) {
    //         let secondPreference = candidateWiseCounts[key]["secondPreferenceCount"];
    //         let thirdPreference = candidateWiseCounts[key]["thirdPreferenceCount"];
    //         let totalCount = candidateWiseCounts[key]["totalCount"];
    //
    //         if (!isNumeric(secondPreference)) {
    //             return false;
    //         }
    //         if (!isNumeric(thirdPreference)) {
    //             return false;
    //         }
    //         if (!isNumeric(totalCount)) {
    //             return false;
    //         }
    //         if (totalCount !== secondPreference + thirdPreference) {
    //             return false;
    //         }
    //     }
    //     return (summary.ballotPapersNotCounted + summary.remainingBallotPapers === summary.total)
    // }

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
                            <div className="page-bottom-fixed-action-bar">
                                <Button
                                    variant="contained" color="default" onClick={handleClickNext(false)}
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
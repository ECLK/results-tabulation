import React, {useState} from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

import Button from '@material-ui/core/Button';
import {
    TALLY_SHEET_ROW_TYPE_BALLOT_BOX,
    TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
    TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX,
    TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A,
    TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B,
    TALLY_SHEET_ROW_TYPE_SITUATION,
    TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT
} from "../constants/TALLY_SHEET_ROW_TYPE";
import {isNumeric, processNumericValue} from "../../../utils";
import {useTallySheetEdit} from "./index";
import Processing from "../../processing";
import Moment from "moment";

export default function TallySheetEdit_CE_201_PV({history, queryString, election, tallySheet, messages}) {

    const MAXIMUM_BALLOT_BOXES_LENGTH = 4;

    const [tallySheetRows, setTallySheetRows] = useState({
        [TALLY_SHEET_ROW_TYPE_BALLOT_BOX]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_SITUATION]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A]: {
            templateRow: {}, map: {}
        },
        [TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B]: {
            templateRow: {}, map: {}
        }
    });


    const handleValueChange = (key, templateRowType, valuePropertyName = "numValue") => event => {
        const {value} = event.target;

        // console.log("####### ", [key, templateRowType, valuePropertyName, value]);
        // debugger;
        setTallySheetRows((tallySheetRows) => {
            tallySheetRows = {...tallySheetRows};
            Object.assign(tallySheetRows[templateRowType].map[key], {[valuePropertyName]: processNumericValue(value)});

            return tallySheetRows;
        });
    };

    const getTallySheetRow = (key, templateRowType) => {
        if (tallySheetRows[templateRowType] && tallySheetRows[templateRowType].map && tallySheetRows[templateRowType].map[key]) {
            return tallySheetRows[templateRowType].map[key];
        }

        return null
    };

    const getValue = (key, templateRowType, valuePropertyName = "numValue") => {
        const tallySheetRow = getTallySheetRow(key, templateRowType);
        if (tallySheetRow) {
            return tallySheetRow[valuePropertyName];
        }

        return 0;
    };


    const setTallySheetContent = async (tallySheetVersion) => {
        try {
            const _tallySheetRows = {...tallySheetRows};

            // Get the `templateRow` assigned to each type of tally sheet rows.
            tallySheet.template.rows.map(((templateRow) => {
                if (_tallySheetRows[templateRow.templateRowType]) {
                    Object.assign(_tallySheetRows[templateRow.templateRowType].templateRow, templateRow)
                }
            }));

            [
                TALLY_SHEET_ROW_TYPE_BALLOT_BOX,
                TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
                TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX,
                TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A,
                TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B,
                TALLY_SHEET_ROW_TYPE_SITUATION,
                TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT
            ].map((templateRowType) => {
                // TODO validate

                let _length = 1;
                if ([
                    TALLY_SHEET_ROW_TYPE_BALLOT_BOX, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
                    TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX
                ].indexOf(templateRowType) >= 0) {
                    _length = MAXIMUM_BALLOT_BOXES_LENGTH;
                }

                for (let i = 0; i < _length; i++) {
                    _tallySheetRows[templateRowType].map[i] = {
                        ..._tallySheetRows[templateRowType].templateRow,
                        ballotBoxId: i,
                        numValue: 0,
                        strValue: ""
                    };
                }

            });


            if (tallySheetVersion) {
                const {content} = tallySheetVersion;

                for (let i = 0; i < content.length; i++) {
                    let contentRow = content[i];

                    if ([
                        TALLY_SHEET_ROW_TYPE_BALLOT_BOX,
                        TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
                        TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX,
                    ].indexOf(contentRow.templateRowType) >= 0 && contentRow.ballotBoxId) {
                        // TODO validate _tallySheetRows
                        Object.assign(_tallySheetRows[contentRow.templateRowType].map[contentRow.ballotBoxId], contentRow)
                    }

                    if ([
                        TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A,
                        TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B,
                        TALLY_SHEET_ROW_TYPE_SITUATION,
                        TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT
                    ].indexOf(contentRow.templateRowType) >= 0) {
                        // TODO validate _tallySheetRows
                        Object.assign(_tallySheetRows[contentRow.templateRowType].map[0], contentRow)
                    }
                }
            }

            debugger;

            setTallySheetRows(_tallySheetRows);
        } catch (e) {
            debugger;
        }
    };

    const validateTallySheetContent = () => {
        // TODO

        return true
    };

    const getTallySheetRequestBody = () => {
        const content = [];
        [
            TALLY_SHEET_ROW_TYPE_BALLOT_BOX,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX
        ].map((templateRowType) => {
            for (let i = 0; i < MAXIMUM_BALLOT_BOXES_LENGTH; i++) {
                const tallySheetRow = getTallySheetRow(i, templateRowType);
                if (tallySheetRow) {
                    content.push(tallySheetRow);
                }
            }
        });
        [
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B,
            TALLY_SHEET_ROW_TYPE_SITUATION,
            TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT
        ].map((templateRowType) => {
            const tallySheetRow = getTallySheetRow(0, templateRowType);
            if (tallySheetRow) {
                content.push(tallySheetRow);
            }
        });

        return {
            content: content
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


    function getTallySheetEditForm() {


        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Serial Number of Postal Votes Ballot Box</TableCell>
                        <TableCell align="center">No. of packets inserted by the Returning Officer</TableCell>
                        <TableCell align="center">No. pf PV-A packets found inside the Ballot Box after the
                            count</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {(() => {
                        const ballotBoxesListJsx = [];
                        for (let i = 0; i < MAXIMUM_BALLOT_BOXES_LENGTH; i++) {
                            ballotBoxesListJsx.push(<TableRow key={i}>
                                <TableCell align="center">
                                    {getValue(i, TALLY_SHEET_ROW_TYPE_BALLOT_BOX, "strValue")}
                                </TableCell>
                                <TableCell align="center">
                                    {getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX)}
                                </TableCell>
                                <TableCell align="center">
                                    {getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX)}
                                </TableCell>
                            </TableRow>);
                        }

                        return ballotBoxesListJsx;
                    })()}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            Total number of PV-A packets found in the Box/ Boxes
                        </TableCell>
                        <TableCell align="right">
                            -- TODO --
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            Number of Packets rejected on various grounds after opening 'A' covers
                        </TableCell>
                        <TableCell align="right">
                            {getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A)}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>No. of covers rejected on</strong>
                            various grounds after opening 'B' covers in accepted ballot papers receptacle
                        </TableCell>
                        <TableCell align="right">
                            {getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B)}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                No of postal ballot papers for the count in the receptacle for accepted ballot papers.
                            </strong>
                        </TableCell>
                        <TableCell align="right">
                            -- TODO --
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                Location of Postal Ballot Paper Counting Centre
                            </strong>
                        </TableCell>
                        <TableCell align="right">
                            {getValue(0, TALLY_SHEET_ROW_TYPE_SITUATION)}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                Time of commencement of the count of Postal Votes ballot papers
                            </strong>
                        </TableCell>
                        <TableCell align="right">
                            {Moment(
                                getValue(0, TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT)
                            ).format('DD-MM-YYYY h:mm A')}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>
                            <div className="page-bottom-fixed-action-bar">
                                <Button variant="contained" color="default" onClick={handleClickBackToEdit()}>
                                    Edit
                                </Button>
                                <Button variant="contained" color="primary" onClick={handleClickSubmit()}>
                                    Submit
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>

                </TableFooter>

            </Table>
        } else if (!processing) {
            const situation = getValue(0, TALLY_SHEET_ROW_TYPE_SITUATION);
            const timeOfCommencementOfCount = getValue(0, TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT);
            const numberOfACoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A);
            const numberOfBCoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B);

            return <Table aria-label="simple table" size="medium">
                <TableHead>
                    <TableRow>
                        <TableCell align="center">Serial Number of Postal Votes Ballot Box</TableCell>
                        <TableCell align="center">No. of packets inserted by the Returning Officer</TableCell>
                        <TableCell align="center">No. pf PV-A packets found inside the Ballot Box after the
                            count</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {(() => {
                        const ballotBoxesListJsx = [];
                        for (let i = 0; i < MAXIMUM_BALLOT_BOXES_LENGTH; i++) {
                            const ballotBoxSerialNumber = getValue(i, TALLY_SHEET_ROW_TYPE_BALLOT_BOX, "strValue");
                            const numberOfPacketsInserted = getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX);
                            const numberOfAPacketsFound = getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX);

                            ballotBoxesListJsx.push(<TableRow key={i}>
                                <TableCell align="center">
                                    <TextField
                                        variant="outlined"
                                        value={ballotBoxSerialNumber}
                                        margin="normal"
                                        onChange={handleValueChange(i, TALLY_SHEET_ROW_TYPE_BALLOT_BOX, "strValue")}
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
                                        error={!isNumeric(numberOfPacketsInserted)}
                                        helperText={!isNumeric(numberOfPacketsInserted) ? "Only numeric values are valid" : ''}
                                        value={numberOfPacketsInserted}
                                        margin="normal"
                                        onChange={handleValueChange(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX)}
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
                                        error={!isNumeric(numberOfAPacketsFound)}
                                        helperText={!isNumeric(numberOfAPacketsFound) ? "Only numeric values are valid" : ''}
                                        value={numberOfAPacketsFound}
                                        margin="normal"
                                        onChange={handleValueChange(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX)}
                                        inputProps={{
                                            style: {
                                                height: '10px'
                                            },
                                        }}
                                    />
                                </TableCell>
                            </TableRow>);
                        }

                        return ballotBoxesListJsx;
                    })()}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            Total number of PV-A packets found in the Box/ Boxes
                        </TableCell>
                        <TableCell align="center">
                            {/*<TextField*/}
                            {/*    required*/}
                            {/*    variant="outlined"*/}
                            {/*    error={calculateTotalNumberOfPVPackets() !== totalNumberOfPVPackets}*/}
                            {/*    helperText={(calculateTotalNumberOfPVPackets() !== totalNumberOfPVPackets) ? "Total count mismatch" : ''}*/}
                            {/*    value={totalNumberOfPVPackets}*/}
                            {/*    margin="normal"*/}
                            {/*    onChange={handleTotalNumberOfPVPacketsChange()}*/}
                            {/*    inputProps={{*/}
                            {/*        style: {*/}
                            {/*            height: '10px'*/}
                            {/*        },*/}
                            {/*    }}*/}
                            {/*/>*/}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            Number of Packets rejected on various grounds after opening 'A' covers
                        </TableCell>
                        <TableCell align="center">
                            <TextField
                                required
                                variant="outlined"
                                error={!isNumeric(numberOfACoversRejected)}
                                helperText={!isNumeric(numberOfACoversRejected) ? "Only numeric values are valid" : ''}
                                value={numberOfACoversRejected}
                                margin="normal"
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A)}
                                inputProps={{
                                    style: {
                                        height: '10px'
                                    },
                                }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>No. of covers rejected on</strong>
                            various grounds after opening 'B' covers in accepted ballot papers receptacle
                        </TableCell>
                        <TableCell align="center">
                            <TextField
                                required
                                variant="outlined"
                                error={!isNumeric(numberOfBCoversRejected)}
                                helperText={!isNumeric(numberOfBCoversRejected) ? "Only numeric values are valid" : ''}
                                value={numberOfBCoversRejected}
                                margin="normal"
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B)}
                                inputProps={{
                                    style: {
                                        height: '10px'
                                    },
                                }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                No of postal ballot papers for the count in the receptacle for accepted ballot papers.
                            </strong>
                        </TableCell>
                        <TableCell align="center">
                            {/*<TextField*/}
                            {/*    required*/}
                            {/*    variant="outlined"*/}
                            {/*    error={!isNumeric(numberOfValidBallotPapers)}*/}
                            {/*    helperText={!isNumeric(numberOfValidBallotPapers) ? "Only numeric values are valid" : ''}*/}
                            {/*    value={numberOfValidBallotPapers}*/}
                            {/*    margin="normal"*/}
                            {/*    onChange={handleNumberOfValidBallotPapersChange()}*/}
                            {/*    inputProps={{*/}
                            {/*        style: {*/}
                            {/*            height: '10px'*/}
                            {/*        },*/}
                            {/*    }}*/}
                            {/*/>*/}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                Location of Postal Ballot Paper Counting Centre
                            </strong>
                        </TableCell>
                        <TableCell align="center">
                            <TextField
                                required
                                variant="outlined"
                                value={situation}
                                margin="normal"
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_SITUATION)}
                                inputProps={{
                                    style: {
                                        height: '10px'
                                    },
                                }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                Time of commencement of the count of Postal Votes ballot papers
                            </strong>
                        </TableCell>
                        <TableCell align="center">
                            <TextField
                                variant="outlined"
                                type='datetime-local'
                                defaultValue={(timeOfCommencementOfCount == null ? "" : Moment(timeOfCommencementOfCount).format('YYYY-MM-DDTHH:mm'))}
                                margin="normal"
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT)}
                                inputProps={{
                                    style: {
                                        height: '10px'
                                    },
                                }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={3}>
                            <div className="page-bottom-fixed-action-bar">
                                <Button variant="contained" color="default" onClick={handleClickNext()}>
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
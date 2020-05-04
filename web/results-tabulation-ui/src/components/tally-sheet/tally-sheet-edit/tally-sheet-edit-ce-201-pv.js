import React, {useState} from "react";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableFooter from "@material-ui/core/TableFooter";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TextField from '@material-ui/core/TextField';

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

    const DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS = "DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS";
    const DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS = "DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS";

    const MAXIMUM_BALLOT_BOXES_LENGTH = 6;

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
        },
        [DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS]: {
            templateRow: {}, map: {}
        },
        [DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS]: {
            templateRow: {}, map: {}
        }
    });


    const getTallySheetRow = (key, templateRowType) => {
        if (tallySheetRows[templateRowType] && tallySheetRows[templateRowType].map && tallySheetRows[templateRowType].map[key]) {
            return tallySheetRows[templateRowType].map[key];
        }

        return null
    };


    const setValue = (key, templateRowType, valuePropertyName = "numValue", value) => {
        setTallySheetRows((tallySheetRows) => {
            tallySheetRows = {...tallySheetRows};
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

        setValue(key, templateRowType, valuePropertyName, value);
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
                TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT,
                DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS,
                DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS
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

            setTallySheetRows(_tallySheetRows);
            setValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS, "numValue",
                calculateTotalNumberOfPVPackets());
            setValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS, "numValue",
                calculateTotalNumberOfValidBallotPapers());

        } catch (e) {
            debugger;
        }
    };

    const validateTallySheetContent = () => {
        let numericFieldsAreValid = true;
        const totalNumberOfPVPackets = getValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS);
        const numberOfValidBallotPapers = getValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS);

        [
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A,
            TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B
        ].map((templateRowType) => {
            for (let key in tallySheetRows[templateRowType].map) {
                if (!isNumeric(tallySheetRows[templateRowType].map[key]["numValue"])) {
                    numericFieldsAreValid = false;
                }
            }
        });

        return numericFieldsAreValid && calculateTotalNumberOfPVPackets() === totalNumberOfPVPackets &&
            calculateTotalNumberOfValidBallotPapers() === numberOfValidBallotPapers
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

    function calculateTotalNumberOfPVPackets() {
        let _numberOfPVPackets = 0;
        for (let i = 0; i < MAXIMUM_BALLOT_BOXES_LENGTH; i++) {
            _numberOfPVPackets += parseInt(getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX));
        }

        return _numberOfPVPackets;
    }

    function calculateTotalNumberOfValidBallotPapers() {
        let _numberOfValidBallotPapers = 0;

        const _numberOfPVPackets = calculateTotalNumberOfPVPackets();
        const numberOfACoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A);
        const numberOfBCoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B);

        _numberOfValidBallotPapers = _numberOfPVPackets - parseInt(numberOfACoversRejected) - parseInt(numberOfBCoversRejected);

        return _numberOfValidBallotPapers;
    }

    const {processing, processingLabel, saved, getActionsBar} = useTallySheetEdit({
        messages,
        history,
        election,
        tallySheet,
        setTallySheetContent,
        validateTallySheetContent,
        getTallySheetRequestBody
    });


    function getTallySheetEditForm() {
        const situation = getValue(0, TALLY_SHEET_ROW_TYPE_SITUATION, "strValue");
        const timeOfCommencementOfCount = getValue(0, TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT, "strValue");
        const numberOfACoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A);
        const numberOfBCoversRejected = getValue(0, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B);

        const totalNumberOfPVPackets = getValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS);
        const numberOfValidBallotPapers = getValue(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS);

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
                            const ballotBoxSerialNumber = getValue(i, TALLY_SHEET_ROW_TYPE_BALLOT_BOX, "strValue");
                            const numberOfPacketsInserted = getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX);
                            const numberOfAPacketsFound = getValue(i, TALLY_SHEET_ROW_TYPE_NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX);

                            ballotBoxesListJsx.push(<TableRow key={i}>
                                <TableCell align="center">
                                    {ballotBoxSerialNumber}
                                </TableCell>
                                <TableCell align="center">
                                    {numberOfPacketsInserted}
                                </TableCell>
                                <TableCell align="center">
                                    {numberOfAPacketsFound}
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
                            {totalNumberOfPVPackets}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            Number of Packets rejected on various grounds after opening 'A' covers
                        </TableCell>
                        <TableCell align="right">
                            {numberOfACoversRejected}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>No. of covers rejected on</strong>
                            various grounds after opening 'B' covers in accepted ballot papers receptacle
                        </TableCell>
                        <TableCell align="right">
                            {numberOfBCoversRejected}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                No of postal ballot papers for the count in the receptacle for accepted ballot papers.
                            </strong>
                        </TableCell>
                        <TableCell align="right">
                            {numberOfValidBallotPapers}
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>
                            <strong>
                                Location of Postal Ballot Paper Counting Centre
                            </strong>
                        </TableCell>
                        <TableCell align="right">
                            {situation}
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
                                timeOfCommencementOfCount
                            ).format('DD-MM-YYYY h:mm A')}
                        </TableCell>
                    </TableRow>
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
                            <TextField
                                required
                                variant="outlined"
                                error={calculateTotalNumberOfPVPackets() !== totalNumberOfPVPackets}
                                helperText={(calculateTotalNumberOfPVPackets() !== totalNumberOfPVPackets) ? "Total count mismatch" : ''}
                                value={totalNumberOfPVPackets}
                                margin="normal"
                                onChange={handleValueChange(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_PV_PACKETS)}
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
                            <TextField
                                required
                                variant="outlined"
                                error={calculateTotalNumberOfValidBallotPapers() !== numberOfValidBallotPapers}
                                helperText={(calculateTotalNumberOfValidBallotPapers() !== numberOfValidBallotPapers) ? "Total count mismatch " : ''}
                                value={numberOfValidBallotPapers}
                                margin="normal"
                                onChange={handleValueChange(0, DERIVED_TALLY_SHEET_ROW_TYPE_NUMBER_OF_VALID_BALLOT_PAPERS)}
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
                                Location of Postal Ballot Paper Counting Centre
                            </strong>
                        </TableCell>
                        <TableCell align="center">
                            <TextField
                                required
                                variant="outlined"
                                value={situation}
                                margin="normal"
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_SITUATION, "strValue")}
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
                                onChange={handleValueChange(0, TALLY_SHEET_ROW_TYPE_TIME_OF_COMMENCEMENT, "strValue")}
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
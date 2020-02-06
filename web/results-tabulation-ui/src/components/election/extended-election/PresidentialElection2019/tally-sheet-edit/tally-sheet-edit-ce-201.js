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

export default function TallySheetEdit_CE_201({history, queryString, election, tallySheet, messages}) {
    const [pollingStationMap, setPollingStationMap] = useState({});
    const [pollingStations, setPollingStations] = useState([]);
    const [totalOrdinaryBallotCountFromBoxCount, setTotalOrdinaryBallotCountFromBoxCount] = useState(0);

    const setTallySheetContent = (tallySheetVersion) => {
        const pollingStations = tallySheet.area.pollingStations;
        const pollingStationMap = {};

        pollingStations.map((pollingStation) => {
            pollingStationMap[pollingStation.areaId] = {
                areaId: pollingStation.areaId,
                ordinaryBallotCountFromBoxCount: 0,
                pollingDistricts: pollingStation.pollingDistricts
            };
        });

        let total = 0;
        if (tallySheetVersion) {
            const {content} = tallySheetVersion;
            for (let i = 0; i < content.length; i++) {
                let contentRow = content[i];
                let {ordinaryBallotCountFromBoxCount} = contentRow;
                if (ordinaryBallotCountFromBoxCount) {
                    pollingStationMap[contentRow.areaId].ordinaryBallotCountFromBoxCount = ordinaryBallotCountFromBoxCount
                    total += ordinaryBallotCountFromBoxCount
                }
            }
        }

        setPollingStations(pollingStations);
        setPollingStationMap(pollingStationMap);
        setTotalOrdinaryBallotCountFromBoxCount(total);
    };

    const validateTallySheetContent = () => {
        for (let key in pollingStationMap) {
            if (!isNumeric(pollingStationMap[key]["ordinaryBallotCountFromBoxCount"])) {
                return false;
            }
        }
        return (calculateTotalOrdinaryBallotCountFromBoxCount() === totalOrdinaryBallotCountFromBoxCount)

    };

    const getTallySheetRequestBody = () => {
        const content = [];

        pollingStations.map(pollingStation => {
            const {areaId} = pollingStation;
            const {ordinaryBallotCountFromBoxCount} = pollingStationMap[areaId];
            content.push({
                areaId: areaId,
                ballotBoxesIssued: [],
                ballotBoxesReceived: [],
                ballotsIssued: 0,
                ballotsReceived: 0,
                ballotsSpoilt: 0,
                ballotsUnused: 0,
                ordinaryBallotCountFromBoxCount: ordinaryBallotCountFromBoxCount,
                tenderedBallotCountFromBoxCount: 0,
                ordinaryBallotCountFromBallotPaperAccount: 0,
                tenderedBallotCountFromBallotPaperAccount: 0
            })
        })

        return {
            content: content
        };
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

    const handleOrdinaryBallotCountFromBoxCountChange = areaId => event => {
        setPollingStationMap({
            ...pollingStationMap,
            [areaId]: {
                ...pollingStationMap[areaId],
                ordinaryBallotCountFromBoxCount: processNumericValue(event.target.value)
            }
        })
    };

    function calculateTotalOrdinaryBallotCountFromBoxCount() {
        let total = 0;
        for (let key in pollingStationMap) {
            total += parseInt(pollingStationMap[key]["ordinaryBallotCountFromBoxCount"])
        }

        return total;
    }

    const handleTotalOrdinaryBallotCountFromBoxCountChange = () => event => {
        setTotalOrdinaryBallotCountFromBoxCount(processNumericValue(event.target.value));
    };

    function getTallySheetEditForm() {
        if (saved) {
            return <Table aria-label="simple table" size={saved ? "small" : "medium"}>
                <TableHead>
                    <TableRow>
                        <TableCell align="left">Polling Districts</TableCell>
                        <TableCell align="left">Polling Station</TableCell>
                        <TableCell align="center">Ordinary Ballot Count</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {pollingStations.map(pollingStation => {
                        const {pollingDistricts, areaName, areaId} = pollingStation;
                        const {ordinaryBallotCountFromBoxCount} = pollingStationMap[areaId];
                        const pollingDistrictsStr = pollingDistricts.map(pollingDistrict => pollingDistrict.areaName).join(", ");
                        return <TableRow key={areaId}>
                            <TableCell align="left">{pollingDistrictsStr}</TableCell>
                            <TableCell align="left">{areaName}</TableCell>
                            <TableCell align="center">{ordinaryBallotCountFromBoxCount}</TableCell>
                        </TableRow>
                    })}
                </TableBody>

                <TableFooter>
                    <TableRow>
                        <TableCell align="right" colSpan={2}>Total ordinary ballot count</TableCell>
                        <TableCell align="right">{totalOrdinaryBallotCountFromBoxCount}</TableCell>
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
            return <Table aria-label="simple table" size="medium">
                <TableHead>
                    <TableRow>
                        <TableCell align="left">Polling Districts</TableCell>
                        <TableCell align="left">Polling Station</TableCell>
                        <TableCell align="center">Ordinary Ballot Count</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {pollingStations.map(pollingStation => {

                        const {pollingDistricts, areaName, areaId} = pollingStation;

                        const {ordinaryBallotCountFromBoxCount} = pollingStationMap[areaId];

                        const pollingDistrictsStr = pollingDistricts.map(pollingDistrict => pollingDistrict.areaName).join(", ");

                        return <TableRow key={areaId}>
                            <TableCell align="left">{pollingDistrictsStr}</TableCell>
                            <TableCell align="left">{areaName}</TableCell>
                            <TableCell align="right">
                                <TextField
                                    required
                                    variant="outlined"
                                    error={!isNumeric(ordinaryBallotCountFromBoxCount)}
                                    helperText={!isNumeric(ordinaryBallotCountFromBoxCount) ? "Only numeric values are valid" : ''}
                                    value={ordinaryBallotCountFromBoxCount}
                                    margin="normal"
                                    onChange={handleOrdinaryBallotCountFromBoxCountChange(areaId)}
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
                        <TableCell align="right" colSpan={2}>Total ordinary ballot count</TableCell>
                        <TableCell align="right">
                            <TextField
                                required
                                error={calculateTotalOrdinaryBallotCountFromBoxCount() !== totalOrdinaryBallotCountFromBoxCount}
                                helperText={calculateTotalOrdinaryBallotCountFromBoxCount() !== totalOrdinaryBallotCountFromBoxCount ? 'Total ballot count mismatch!' : ' '}
                                value={totalOrdinaryBallotCountFromBoxCount}
                                margin="normal"
                                onChange={handleTotalOrdinaryBallotCountFromBoxCountChange()}
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
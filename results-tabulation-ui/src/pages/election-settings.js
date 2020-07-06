import React, {useEffect, useState} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import ExtendedElection from "../components/election/extended-election";
import TabulationPage from "./index";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField/TextField";
import Divider from '@material-ui/core/Divider';
import {Link} from "react-router-dom";
import {getAreas} from "../services/tabulation-api";
import Processing from "../components/processing";
import Error from "../components/error";
import {PATH_ELECTION_BY_ID} from "../App";

export default function ElectionSettings(props) {
    const {election} = props;
    const {electionId, electionName} = election;

    const [electoralDistricts, setElectoralDistricts] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        getAreas({electionId: electionId, areaType: "ElectoralDistrict"}).then((electoralDistricts) => {
            setElectoralDistricts(electoralDistricts);
            setProcessing(false);
        }).catch((error) => {
            setError(error);
            setProcessing(false);
        });
    }, []);

    function getElectionSettingsJsx() {
        if (processing) {
            return <Processing/>
        } else if (error) {
            return <Error
                error={error}
            />
        } else if (electoralDistricts.length === 0) {
            return <Error
                title={"Oops.."}
                body="No electoral districts available or authorized to access."
            />
        } else {
            return electoralDistricts.map(({areaId, areaName}) => {
                return <div key={areaId}>
                    <Divider/>
                    <h2>{areaName}</h2>
                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell align="center">
                                        <TextField
                                            style={{width: "100%"}}
                                            margin="dense"
                                            variant="outlined"
                                            placeholder="User"
                                        />
                                    </TableCell>
                                    <TableCell align="center">
                                        <TextField
                                            style={{width: "100%"}}
                                            margin="dense"
                                            variant="outlined"
                                            placeholder="NIC"
                                        />
                                    </TableCell>
                                    <TableCell align="center">
                                        <TextField
                                            style={{width: "100%"}}
                                            margin="dense"
                                            variant="outlined"
                                            placeholder="Mobile"
                                        />
                                    </TableCell>
                                    <TableCell align="center">Data Entry</TableCell>
                                    <TableCell align="center">PD View</TableCell>
                                    <TableCell align="center">PD Verify</TableCell>
                                    <TableCell align="center">ED View</TableCell>
                                    <TableCell align="center">ED Verify</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((userId) => {
                                    return <TableRow key={userId}>
                                        <TableCell>Dinuka, De Silva (dinukadesilva)</TableCell>
                                        <TableCell>930273295V</TableCell>
                                        <TableCell>0778531196</TableCell>
                                        <TableCell align="center" padding="none">
                                            <Checkbox checked={true} onChange={() => {
                                            }}/>
                                        </TableCell>
                                        <TableCell align="center" padding="none">
                                            <Checkbox checked={true} onChange={() => {
                                            }}/>
                                        </TableCell>
                                        <TableCell align="center" padding="none">
                                            <Checkbox checked={true} onChange={() => {
                                            }}/>
                                        </TableCell>
                                        <TableCell align="center" padding="none">
                                            <Checkbox checked={true} onChange={() => {
                                            }}/>
                                        </TableCell>
                                        <TableCell align="center" padding="none">
                                            <Checkbox checked={true} onChange={() => {
                                            }}/>
                                        </TableCell>

                                    </TableRow>
                                })}
                                <TableRow>
                                    <TableCell colSpan={8} style={{textAlign: "center"}}>
                                        <Button variant="outlined" color="secondary">
                                            Add new district user to
                                            <strong style={{paddingLeft: 5}}> {areaName} </strong>
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            });
        }
    }

    return <TabulationPage>
        <div className="page-content">

            <h1>{electionName} / Settings</h1>

            {getElectionSettingsJsx()}
        </div>
    </TabulationPage>
}

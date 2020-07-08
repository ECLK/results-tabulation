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
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import {Link} from "react-router-dom";
import {getAreas} from "../services/tabulation-api";
import Processing from "../components/processing";
import Error from "../components/error";
import {PATH_ELECTION_BY_ID} from "../App";


export default function ElectionSettings(props) {
    const {election} = props;
    const {electionId, electionName} = election;

    const [electoralDistrictsList, setElectoralDistrictsList] = useState([]);
    const [electoralDistrictsMap, setElectoralDistrictsMap] = useState({});
    const [countryList, setCountryList] = useState([]);
    const [countryMap, setCountryMap] = useState({});

    const [selectedAreaId, setSelectedAreaId] = useState(null);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    const handleChange = (event, newValue) => {
        setSelectedAreaId(newValue);
    };

    async function fetchData() {
        try {
            const _electoralDistrictsList = await getAreas({electionId: electionId, areaType: "ElectoralDistrict"});
            const _electoralDistrictsMap = {};
            for (let i = 0; i < _electoralDistrictsList.length; i++) {
                _electoralDistrictsMap[_electoralDistrictsList[i].areaId] = _electoralDistrictsList[i];
            }

            setElectoralDistrictsList(_electoralDistrictsList);
            setElectoralDistrictsMap(_electoralDistrictsMap);

            const _countryList = await getAreas({electionId: electionId, areaType: "Country"});
            const _countryMap = {};
            for (let i = 0; i < _countryList.length; i++) {
                _countryMap[_countryList[i].areaId] = _countryList[i];
            }

            setCountryList(_countryList);
            setCountryMap(_countryMap);

            setProcessing(false);
        } catch (error) {
            setError(error);
            setProcessing(false);
        }
    }

    useEffect(() => {
        fetchData()
    }, []);

    function getTabContent() {
        if (selectedAreaId) {
            if (electoralDistrictsMap[selectedAreaId]) {
                const selectedElectoralDistrict = electoralDistrictsMap[selectedAreaId];
                const {areaName} = selectedElectoralDistrict;
                return <div>
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
            } else if (countryMap[selectedAreaId]) {
                const selectedCountry = countryMap[selectedAreaId];
                const {areaName} = selectedCountry;
                return <div>
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
                                    <TableCell align="center">AI View</TableCell>
                                    <TableCell align="center">AI Verify</TableCell>
                                    <TableCell align="center">EC Leadership</TableCell>
                                    <TableCell align="center">Admin</TableCell>
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
            }
        }
    }

    function getElectionSettingsJsx() {
        if (processing) {
            return <Processing/>
        } else if (error) {
            return <Error
                error={error}
            />
        } else if (electoralDistrictsList.length === 0) {
            return <Error
                title={"Oops.."}
                body="No electoral districts available or authorized to access."
            />
        } else {
            return <div style={{display: "flex", minHeight: 400}}>
                <Tabs
                    orientation="vertical"
                    variant="scrollable"
                    value={selectedAreaId}
                    onChange={handleChange}
                    aria-label="Vertical tabs example"
                    style={{borderRight: "1px solid #e0e0e0"}}
                >
                    <strong style={{fontSize: 9}}>Electoral Districts</strong>
                    {electoralDistrictsList.map(({areaId, areaName}) => {
                        return <Tab key={areaId} label={areaName} value={areaId} style={{textAlign: "left"}}/>
                    })}
                    <Divider/>
                    <strong style={{fontSize: 9}}>National</strong>
                    {countryList.map(({areaId, areaName}) => {
                        return <Tab key={areaId} label={areaName} value={areaId} style={{textAlign: "left"}}/>
                    })}
                </Tabs>
                <div style={{flex: 1, overflow: "auto", paddingLeft: 12}}>
                    {getTabContent()}
                </div>
            </div>;
        }
    }

    return <TabulationPage>
        <div className="page-content">

            <h1>{electionName} / Settings</h1>

            {getElectionSettingsJsx()}
        </div>
    </TabulationPage>
}

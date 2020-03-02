import React, {useEffect, useState} from "react";
import {getElections} from "../services/tabulation-api";
import {Link} from "react-router-dom";
import {PATH_ELECTION_BY_ID} from "../App";
import Processing from "../components/processing";
import Error from "../components/error";
import TabulationPage from "./index";


export default function Home() {
    const [electionsList, setElectionsList] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);


    // Similar to componentDidMount and componentDidUpdate:
    useEffect(() => {
        getElections({}).then((electionsList) => {
            setElectionsList(electionsList);
            setProcessing(false);
        }).catch(() => {
            setError(true);
            setProcessing(false);
        })
    }, []);

    function getElectionListJsx() {
        if (processing) {
            return <Processing/>
        } else if (error) {
            return <Error
                title="Tally sheet list cannot be accessed."
            />
        } else if (electionsList.length === 0) {
            return <Error
                title="No elections available or authorized to access."
            />
        } else {
            return <div className="election-list">
                {electionsList.map((election) => {
                    const {electionId, electionName} = election;

                    return <Link
                        key={electionId} to={PATH_ELECTION_BY_ID(electionId)}
                        className="election-list-item"
                    >
                        {electionName}
                    </Link>
                })}
            </div>
        }
    }

    return <TabulationPage>
        <div className="page-content">
            {getElectionListJsx()}
        </div>
    </TabulationPage>
}

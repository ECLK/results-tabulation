import React, {useContext, useEffect, useState} from "react";
import {Link} from "react-router-dom";
import {PATH_ELECTION_BY_ID} from "../App";
import Processing from "../components/processing";
import Error from "../components/error";
import TabulationPage from "./index";
import {ElectionContext} from "../services/election.provider";


export default function Home() {
    const electionContext = useContext(ElectionContext);

    const [electionsList, setElectionsList] = useState([]);
    const [processing, setProcessing] = useState(true);
    const [error, setError] = useState(false);

    // Similar to componentDidMount and componentDidUpdate:
    useEffect(() => {
        electionContext.getElections({isListed: true, parentElectionId: null}).then((electionsList) => {
            setElectionsList(electionsList.filter(({electionId, rootElectionId}) => {
                return electionId === rootElectionId;
            }));
            setProcessing(false);
        }).catch((error) => {
            setError(error);
            setProcessing(false);
        })
    }, []);

    function getElectionListJsx() {
        if (processing) {
            return <Processing/>
        } else if (error) {
            return <Error
                error={error}
            />
        } else if (electionsList.length === 0) {
            return <Error
                title={"Oops.."}
                body="No elections available or authorized to access."
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

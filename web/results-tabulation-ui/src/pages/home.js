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
    const groups = [];


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

          // get the root elections
          {electionsList.map(election => {
            if (election.electionId === election.rootElectionId) {
                var root = {
                  "rootElectionId" : election.electionId,
                  "rootElectionName" : election.electionName
                }
                groups.push(root);
            }
          })}

            return <div className="election-list">
              {groups.map((group,index) => {
                return(
                  <div className="election-panel" key={index}>
                    <div className="root-election">
                      <Link to={PATH_ELECTION_BY_ID(group.rootElectionId)}
                        className="election-list-item">
                        {group.rootElectionName}
                      </Link>
                    </div>
                    <div className="sub-elections">
                      <div className="election-list-item-children">
                          {electionsList
                            .filter(election => election.electionId !== group.rootElectionId)
                            .map(election => {
                              const {electionId, electionName} = election;
                              return(
                                <React.Fragment>
                                <Link key={electionId} to={PATH_ELECTION_BY_ID(electionId)}
                                  className="election-list-item">
                                  {electionName}
                                </Link>
                                <Link key={electionId} to={PATH_ELECTION_BY_ID(electionId)}
                                  className="election-list-item">
                                  {electionName}
                                </Link>
                                </React.Fragment>
                              )
                            })
                          }
                      </div>
                    </div>
                  </div>
              )
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

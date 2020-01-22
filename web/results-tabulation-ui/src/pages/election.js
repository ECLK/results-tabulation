import BreadCrumb from "../components/bread-crumb";
import {PATH_ELECTION, PATH_ELECTION_BY_ID} from "../App";
import React from "react";
import ExtendedElection from "../components/election/extended-election";

export default function Election(props) {
    const {election} = props;
    const {electionId, electionName} = election;
    const extendedElection = ExtendedElection(election);

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: electionName, to: PATH_ELECTION_BY_ID(electionId)}
            ]}
        />
        {extendedElection.getElectionHome()}
    </div>
}
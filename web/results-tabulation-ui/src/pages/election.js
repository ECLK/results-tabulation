import BreadCrumb from "../components/bread-crumb";
import {PATH_ELECTION, PATH_ELECTION_BY_ID} from "../App";
import React from "react";
import {ElectionHome} from "../components/election/election-menu";

export default function Election(props) {
    const {election} = props;
    const {electionId, electionName} = election;

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: electionName, to: PATH_ELECTION_BY_ID(electionId)}
            ]}
        />
        <ElectionHome election={election}/>
    </div>
}
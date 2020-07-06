import React from "react";
import ExtendedElection from "../components/election/extended-election";
import TabulationPage from "./index";
import "./election.css";

export default function Election(props) {
    const {election} = props;
    const extendedElection = ExtendedElection(election);

    return <TabulationPage election={election}>
        {extendedElection.getElectionHome()}
    </TabulationPage>
}

import {PATH_ELECTION, PATH_ELECTION_BY_ID} from "../App";
import React, {Component} from "react";
import BreadCrumb from "../components/bread-crumb";

function getBreadCrumbLinks(election, additionalLinks) {
    let _election = election;
    let _electionLinks = [];
    while (_election) {
        if (_election.isListed) {
            _electionLinks.unshift({
                label: _election.electionName, to: PATH_ELECTION_BY_ID(_election.electionId)
            });
        }

        _election = _election.parentElection;
    }

    const breadCrumbLinks = [
        {label: "elections", to: PATH_ELECTION()},
        ..._electionLinks,
        ...additionalLinks
    ];

    return breadCrumbLinks;
}

export default class TabulationPage extends Component {
    render() {
        const {election, additionalBreadCrumbLinks = [], children} = this.props;

        return <div className="page">
            <BreadCrumb
                links={getBreadCrumbLinks(election, additionalBreadCrumbLinks)}
            />
            {children}
        </div>
    }
}

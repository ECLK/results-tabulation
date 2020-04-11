import {PATH_ELECTION, PATH_ELECTION_BY_ID, PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW} from "../App";
import React, {Component} from "react";
import BreadCrumb from "../components/bread-crumb";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import IconButton from "@material-ui/core/IconButton";
import InfoIcon from "@material-ui/icons/Info";


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


export function TabulationTallySheetPage(props) {
    const {election, additionalBreadCrumbLinks = [], tallySheet, history, children} = props;

    const {tallySheetId, tallySheetCode} = tallySheet;
    const {rootElection, voteType} = election;

    return <div className="page">
        <BreadCrumb
            links={getBreadCrumbLinks(election, additionalBreadCrumbLinks)}
        />
        <div className="tally-sheet-page-header">
            <h4 className="tally-sheet-page-header-election">{rootElection.electionName}</h4>
            <strong className="tally-sheet-page-header-tally-sheet-code">
                {getTallySheetCodeStr({tallySheetCode, voteType})}
            </strong>
            <h5 className="tally-sheet-page-header-area">{tallySheet.area.areaName}</h5>
            <IconButton
                aria-label="delete" style={{float: "right"}}
                className="tally-sheet-page-header-info-link"
                onClick={() => {
                    history.push(PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW(tallySheetId))
                }}
            >
                <InfoIcon/>
            </IconButton>
        </div>
        {children}
    </div>
}

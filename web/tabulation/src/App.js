import React, {useContext} from 'react';
import './App.css';
import NavBar from "./components/navbar/Navbar";

import {Redirect, Switch} from "react-router";
import {ElectionProtectedRoute, ProtectedRoute, TallySheetProtectedRoute} from "./auth";

import Home from "./pages/home"
import Election from "./pages/election";
import DataEntryList from "./pages/data-entry-list";
import DataEntryEdit from "./pages/data-entry-edit";
import ReportList from "./pages/report-list";
import ReportView from "./pages/report-view";
import ReleaseView from "./pages/release-view";
import ReleaseList from "./pages/release-list";
import Processing from "./components/processing";

export const ROUTER_PREFIX = "";
export const PATH_ELECTION = () => `${ROUTER_PREFIX}/election`;
export const PATH_ELECTION_BY_ID = (electionId) => `${ROUTER_PREFIX}/election/${electionId}`;
export const PATH_ELECTION_DATA_ENTRY = (electionId, tallySheetCode = null, subElectionId = null) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/data-entry`;
    if (tallySheetCode) {
        path += `?tallySheetCode=${tallySheetCode}&`;
    }

    if (subElectionId) {
        path += `subElectionId=${subElectionId}&`;
    }

    return path;
};
export const PATH_ELECTION_DATA_ENTRY_EDIT = (electionId, tallySheetId, tallySheetVersionId) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/data-entry/${tallySheetId}`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`
    }

    return path
};
export const PATH_ELECTION_VERIFICATION = (electionId, tallySheetCode) => {
    return `${ROUTER_PREFIX}/election/${electionId}/verification?tallySheetCode=${tallySheetCode}`;
};
export const PATH_ELECTION_VERIFICATION_EDIT = (electionId, tallySheetId) => {
    return `${ROUTER_PREFIX}/election/${electionId}/verification/${tallySheetId}`;
};
export const PATH_ELECTION_REPORT = (electionId, tallySheetCode, subElectionId) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/report`;
    if (tallySheetCode) {
        path += `?tallySheetCode=${tallySheetCode}&`;
    }

    if (subElectionId) {
        path += `subElectionId=${subElectionId}&`;
    }

    return path;
};
export const PATH_ELECTION_RESULTS_RELEASE = (electionId, tallySheetCode, subElectionId) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/release`;
    if (tallySheetCode || subElectionId) {
        path += '?';
    }

    if (tallySheetCode) {
        path += `tallySheetCode=${tallySheetCode}`;
    }

    if (tallySheetCode && subElectionId) {
        path += '&';
    }

    if (subElectionId) {
        path += `subElectionId=${subElectionId}`;
    }

    return path;
};

export const PATH_ELECTION_RESULTS_RELEASE_VIEW = (electionId, tallySheetId) => {
    return `${ROUTER_PREFIX}/election/${electionId}/release/${tallySheetId}`;
};

export const PATH_ELECTION_REPORT_VIEW = (electionId, tallySheetId) => {
    return `${ROUTER_PREFIX}/election/${electionId}/report/${tallySheetId}`;
};

// export const PATH_ELECTION_TALLY_SHEET_REVIEW = (electionId, tallySheetId) => {
//     return `${ROUTER_PREFIX}/election/${electionId}/tallySheet-/${tallySheetId}`;
// };

export const TALLY_SHEET_CODE_PRE_34_CO = "PRE-34-CO";
export const TALLY_SHEET_CODE_PRE_34 = "PRE-34";
export const TALLY_SHEET_CODE_PRE_34_I_RO = "PRE-34-I-RO";
export const TALLY_SHEET_CODE_PRE_34_II_RO = "PRE-34-II-RO";
export const TALLY_SHEET_CODE_PRE_34_PD = "PRE-34-PD";
export const TALLY_SHEET_CODE_PRE_34_ED = "PRE-34-ED";
export const TALLY_SHEET_CODE_PRE_34_AI = "PRE-34-AI";
export const TALLY_SHEET_CODE_PRE_41 = "PRE-41";
export const TALLY_SHEET_CODE_CE_201 = "CE-201";
export const TALLY_SHEET_CODE_CE_201_PV = "CE-201-PV";
export const TALLY_SHEET_CODE_PRE_30_PD = "PRE-30-PD";
export const TALLY_SHEET_CODE_PRE_30_PV = "PRE-30-PV";
export const TALLY_SHEET_CODE_PRE_30_ED = "PRE-30-ED";
export const TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS = "PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS";
export const TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS = "PRE-ALL-ISLAND-RESULTS";

export const COUNTING_CENTRE_WISE_DATA_ENTRY_TALLY_SHEET_CODES = [
    TALLY_SHEET_CODE_PRE_41, TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_CE_201_PV, TALLY_SHEET_CODE_PRE_34_CO
];

export const DIVISIONAL_TALLY_SHEET_CODES = [
    TALLY_SHEET_CODE_PRE_30_PD
];

export const DISTRICT_TALLY_SHEET_CODES = [
    TALLY_SHEET_CODE_PRE_30_ED, TALLY_SHEET_CODE_PRE_30_PV
];

export const ALL_ISLAND_TALLY_SHEET_CODES = [
    TALLY_SHEET_CODE_PRE_30_ED, TALLY_SHEET_CODE_PRE_30_PV
];

function App() {

    function getHeader() {
        if (ProtectedRoute.isAuthenticated()) {
            return <NavBar/>
        } else {
            return <div className="fixed-loading-page">
                Loading ...
            </div>
        }
    }

    return (
        <div>
            {getHeader()}
            <Switch>

                <Redirect exact path="/" to={PATH_ELECTION()}/>


                <ProtectedRoute
                    exact
                    path={PATH_ELECTION()}
                    component={Home}
                />
                <ElectionProtectedRoute
                    exact
                    path={PATH_ELECTION_BY_ID(":electionId")}
                    component={Election}
                />
                <ElectionProtectedRoute
                    exact
                    path={PATH_ELECTION_DATA_ENTRY(":electionId")}
                    component={DataEntryList}
                />
                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_DATA_ENTRY_EDIT(":electionId", ":tallySheetId", ":tallySheetVersionId?")}
                    component={DataEntryEdit}
                />
                <ElectionProtectedRoute
                    exact
                    path={PATH_ELECTION_REPORT(":electionId")}
                    component={ReportList}
                />

                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_REPORT_VIEW(":electionId", ":tallySheetId")}
                    component={ReportView}
                />

                <ElectionProtectedRoute
                    exact
                    path={PATH_ELECTION_RESULTS_RELEASE(":electionId")}
                    component={ReleaseList}
                />

                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_RESULTS_RELEASE_VIEW(":electionId", ":tallySheetId")}
                    component={ReleaseView}
                />

            </Switch>
        </div>
    );
}

export default App;

import React from 'react';
import './App.css';
import NavBar from "./components/navbar/Navbar";

import {Redirect, Switch} from "react-router";
import {ElectionProtectedRoute, ProtectedRoute, TallySheetProtectedRoute} from "./auth";

import Home from "./pages/home"
import Election from "./pages/election";
import ReleaseView from "./pages/release-view";
import ReleaseList from "./pages/release-list";
import TallySheetListView from "./pages/tally-sheet-list-view";
import TallySheetView from "./pages/tally-sheet-view";

export const ROUTER_PREFIX = "";
export const PATH_ELECTION = () => `${ROUTER_PREFIX}/election`;
export const PATH_ELECTION_BY_ID = (electionId) => `${ROUTER_PREFIX}/election/${electionId}`;
export const PATH_ELECTION_TALLY_SHEET_LIST = (electionId, tallySheetCode = null) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/tally-sheet`;
    if (tallySheetCode) {
        path += `?tallySheetCode=${tallySheetCode}&`;
    }

    return path;
};
export const PATH_ELECTION_VERIFICATION = (electionId, tallySheetCode) => {
    return `${ROUTER_PREFIX}/election/${electionId}/verification?tallySheetCode=${tallySheetCode}`;
};
export const PATH_ELECTION_VERIFICATION_EDIT = (electionId, tallySheetId) => {
    return `${ROUTER_PREFIX}/election/${electionId}/verification/${tallySheetId}`;
};
export const PATH_ELECTION_RESULTS_RELEASE = (electionId, tallySheetCode) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/release`;

    if (tallySheetCode) {
        path += `?tallySheetCode=${tallySheetCode}`;
    }

    return path;
};

export const PATH_ELECTION_RESULTS_RELEASE_VIEW = (electionId, tallySheetId) => {
    return `${ROUTER_PREFIX}/election/${electionId}/release/${tallySheetId}`;
};

export const PATH_ELECTION_TALLY_SHEET_VIEW = (electionId, tallySheetId, tallySheetVersionId) => {
    let path = `${ROUTER_PREFIX}/election/${electionId}/tally-sheet/${tallySheetId}`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`
    }

    return path
};


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
                    path={PATH_ELECTION_TALLY_SHEET_LIST(":electionId")}
                    component={TallySheetListView}
                />
                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_TALLY_SHEET_VIEW(":electionId", ":tallySheetId", ":tallySheetVersionId?")}
                    component={TallySheetView}
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

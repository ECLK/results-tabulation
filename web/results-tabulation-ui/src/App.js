import React from 'react';
import './App.css';
import NavBar from "./components/navbar/Navbar";

import {Redirect, Switch} from "react-router";
import {ElectionProtectedRoute, ProtectedRoute, TallySheetProtectedRoute} from "./auth";

import Home from "./pages/home"
import Election from "./pages/election";
import TallySheetListView from "./pages/tally-sheet-list-view";
import TallySheetView from "./pages/tally-sheet-view";
import TallySheetActivityView from "./pages/tally-sheet-activity";
import * as serviceWorker from "./serviceWorker";

export const ROUTER_PREFIX = "";
export const PATH_ELECTION = () => `${ROUTER_PREFIX}/election`;
export const PATH_ELECTION_BY_ID = (electionId) => `${ROUTER_PREFIX}/election/${electionId}`;
export const PATH_ELECTION_TALLY_SHEET_LIST = (electionId = null, tallySheetCode = null, voteType = null) => {
    let path = `${ROUTER_PREFIX}/tally-sheet`;
    if (tallySheetCode) {
        path += `?tallySheetCode=${tallySheetCode}&`;
    }
    if (electionId) {
        path += `electionId=${electionId}&`;
    }
    if (voteType) {
        path += `voteType=${voteType}&`;
    }

    return path;
};

export const PATH_ELECTION_TALLY_SHEET_VIEW = (tallySheetId, tallySheetVersionId) => {
    let path = `${ROUTER_PREFIX}/tally-sheet/${tallySheetId}`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`
    }

    return path
};

export const PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW = (tallySheetId) => {
    return `${ROUTER_PREFIX}/tally-sheet-activity/${tallySheetId}`;
};

function App() {

    function getHeader() {
        if (ProtectedRoute.isAuthenticated()) {
            return <NavBar/>
        } else {

            // As a fix for https://github.com/ECLK/results-tabulation-api/issues/519
            // Unregistering the service worker enable the app redirecting to external urls.
            serviceWorker.unregister();

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
                    path={PATH_ELECTION_TALLY_SHEET_LIST()}
                    component={TallySheetListView}
                />
                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_TALLY_SHEET_VIEW(":tallySheetId", ":tallySheetVersionId?")}
                    component={TallySheetView}
                />
                <TallySheetProtectedRoute
                    exact
                    path={PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW(":tallySheetId")}
                    component={TallySheetActivityView}
                />
            </Switch>
        </div>
    );
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {BrowserRouter} from "react-router-dom";
import {Router} from "react-router";
import {history} from "./utils";
import {MessagesProvider} from "./services/messages.provider";
import {TallySheetProvider} from "./services/tally-sheet.provider";
import {DialogProvider} from "./services/dialog.provider";

ReactDOM.render(
    <DialogProvider>
        <MessagesProvider>
            <TallySheetProvider>
                <BrowserRouter>
                    <Router history={history}>
                        <App/>
                    </Router>
                </BrowserRouter>
            </TallySheetProvider>
        </MessagesProvider>
    </DialogProvider>
    , document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register();

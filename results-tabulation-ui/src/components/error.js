import React from "react";
import WarningIcon from '@material-ui/icons/Warning';
import {getErrorCode, getErrorMessage} from "../utils";
import "./error.css"


export default function Error(
    {
        title,
        body,
        error
    }
) {

    if (!body) {
        body = <>
            This could be because you are trying to access a resource you aren't authorized.
            <br/><br/>
            <small>Check your internet connection.</small>
        </>
    }

    if (!title) {
        title = "[Error] Unknown error."
    }

    if (error) {
        const errorCode = getErrorCode(error);
        if (errorCode) {
            let _body = getErrorMessage(errorCode);
            if (_body) {
                title = `[Error] ${errorCode}`;
                body = _body
            }
        }
    }

    return <div className="tabulation-page-message">
        <WarningIcon style={{fontSize: 55, padding: "0px 40px", color: "#FFC107"}}/>
        <div className="tabulation-page-message-content">
            <strong>{title}</strong>
            <p>{body}</p>
        </div>
    </div>
}
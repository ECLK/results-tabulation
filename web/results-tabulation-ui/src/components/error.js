import React from "react";
import WarningIcon from '@material-ui/icons/Warning';


export default function Error(
    {
        title,
        body
    }
) {
    if (!body) {
        body = <>
            This could be because you are trying to access a resource you aren't authorized.
            <br/><small>Check your internet connection.</small>
        </>
    }

    if (!title) {
        title = "[Error] Unknown error."
    }

    return <div className="tabulation-page-message">
        <WarningIcon style={{fontSize: 55, padding: "0px 40px", color: "#FFC107"}}/>
        <div className="tabulation-page-message-content">
            <strong>{title}</strong>
            <p>{body}</p>
        </div>
    </div>
}
import React from "react";


export default function Error(
    {
        title,
        body = "This could be because you are trying to access a resource you aren't authorized."
    }
) {
    return <div className="tabulation-page-message">
        <strong>{title}</strong>
        <p>{body}</p>

        <small>Check your internet connection.</small>
    </div>
}
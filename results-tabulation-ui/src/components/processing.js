import React from "react";
import LinearProgress from '@material-ui/core/LinearProgress';

/**
 *
 * @param label = "Loading ... "
 *          Label being displayed with the progress bar.
 * @param showProgress = true
 *          A boolean indicating whether to show or hide the progress bar.
 * @param showContent = true
 *          A boolean indicating whether to show the content after.
 * @param children
 *          Content.
 * @returns {*}
 * @constructor
 */
export default function Processing(
    {
        label = "Loading ... ",
        showProgress = true,
        showContent = true,
        children = null
    }
) {

    if (showProgress) {
        return [
            <div className="tabulation-linear-progress-bar" key="1">
                <div className="tabulation-linear-progress-bar-label">{label}</div>
                <LinearProgress/>
                <div className="tabulation-linear-progress-bar-content">
                </div>
            </div>,
            showContent ? children : null
        ];
    } else {
        return children;
    }

}


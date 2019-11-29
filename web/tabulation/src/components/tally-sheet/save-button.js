import React, {useEffect, useState} from "react";
import Button from "@material-ui/core/Button";

export default function SaveButton(props) {
    const {fetchHtml} = props;

    const {tallySheetId, tallySheetVersionId, children, onProcessing, tallySheet, setTallySheet} = props;
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        onProcessing && onProcessing(processing);
    }, [processing])

    const handleOnClick = () => async (event) => {
        setProcessing(true);

        // TODO

        setProcessing(false);
    };

    return <Button
        variant={props.variant}
        color={props.color}
        size={props.size}
        disabled={processing}
        onClick={handleOnClick()}
    >
        {children}
    </Button>
}

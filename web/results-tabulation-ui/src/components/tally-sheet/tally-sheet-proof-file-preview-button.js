import React, {useContext, useState} from "react";
import Button from "@material-ui/core/Button";
import {TallySheetProofFilePreviewDialog} from "./tally-sheet-proof-file-preview-dialog";
import {DialogContext} from "../../services/dialog.provider";
import {MessagesContext} from "../../services/messages.provider";

export default function PreviewTallySheetProofFileButton(props) {
    const dialogContext = useContext(DialogContext);
    const messageContext = useContext(MessagesContext);


    const {tallySheetId, fileId, children} = props;
    const [open, setOpen] = useState(false);

    const onClick = (open = false) => async (evt) => {
        await dialogContext.push({
            render({open, handleClose, handleOk}) {
                return <TallySheetProofFilePreviewDialog tallySheetId={tallySheetId} fileId={fileId} open={open}
                                                         handleClose={handleClose}/>
            }
        })
    };

    return <Button
        {...props}
        onClick={onClick(true)}
    >=
        {children}
    </Button>
}

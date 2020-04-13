import React, {useContext, useEffect, useState} from "react";
import Slide from "@material-ui/core/Slide";
import Dialog from "@material-ui/core/Dialog";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Typography from "@material-ui/core/Typography";
import DialogContent from "@material-ui/core/DialogContent";
import {TallySheetContext} from "../../services/tally-sheet.provider";


export function TallySheetProofFilePreviewDialog({tallySheetId, open, fileId, handleClose}) {
    const tallySheetContext = useContext(TallySheetContext);

    const [file, setFile] = useState({});

    useEffect(() => {
        tallySheetContext.getTallySheetProofFileDataUrl(tallySheetId, fileId).then(file => setFile(file));
    }, [tallySheetId, fileId]);

    return <Dialog
        open={open} fullScreen style={{backgroundColor: "transparent"}}
        PaperProps={{
            style: {backgroundColor: "transparent"}
        }}
        onBackdropClick={handleClose()}
    >
        <div style={{display: "flex", flex: 0, padding: 15, backgroundColor: "black"}}>
            <Typography variant="h5" style={{flex: 1, color: "white"}}>{file.fileName}</Typography>
            <IconButton aria-label="close" onClick={handleClose()} style={{color: "white"}}>
                <CloseIcon/>
            </IconButton>
        </div>

        <DialogContent onClick={handleClose()} style={{
            backgroundColor: "transparent",
            paddingLeft: 40,
            paddingRight: 40,
            paddingBottom: 0,
            paddingTop: 0
        }}>
            <iframe
                width={"100%"}
                src={file.dataUrl}
                style={{backgroundColor: "black", border: "none", minHeight: "100%"}}
                onClick={(evt) => evt.preventDefault()}
            />
        </DialogContent>
    </Dialog>
}
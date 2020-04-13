import React, {useContext, useEffect, useState} from "react";
import Slide from "@material-ui/core/Slide";
import Dialog from "@material-ui/core/Dialog";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import {MESSAGES_EN} from "../../../locale/messages_en";
import {MESSAGE_TYPES, MessagesContext} from "../../../services/messages.provider";
import {TallySheetContext} from "../../../services/tally-sheet.provider";
import {DialogContext} from "../../../services/dialog.provider";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemText from '@material-ui/core/ListItemText';
import PictureAsPdfIcon from '@material-ui/icons/PictureAsPdf';
import ImageIcon from '@material-ui/icons/Image';
import DescriptionIcon from '@material-ui/icons/Description';
import PreviewTallySheetProofFileButton from "../tally-sheet-proof-file-preview-button";
import Processing from "../../processing";

export function UploadTallySheetProofsDialog(
    {
        tallySheetId, open, handleClose, handleOk, allowUpload = true, title = "Upload Documents",
        actions = [{value: "Done", onClick: handleClose}]
    }
) {
    const tallySheetContext = useContext(TallySheetContext);
    const messageContext = useContext(MessagesContext);

    const [processing, setProcessing] = useState(true);
    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);

    const [files, setFiles] = useState([]);

    const Transition = React.forwardRef(function Transition(props, ref) {
        return <Slide direction="up" ref={ref} {...props} />;
    });

    useEffect(() => {
        fetchFiles();
    }, [tallySheet]);

    async function fetchFiles() {
        setProcessing(true);
        try {
            const scannedFiles = tallySheet.workflowInstance.proof.scannedFiles;
            const _files = [];
            for (let i = 0; i < scannedFiles.length; i++) {
                const fileId = scannedFiles[i].fileId;
                const file = await tallySheetContext.getTallySheetProofFileDataUrl(tallySheetId, fileId);
                _files.push(file);
            }

            setFiles(_files);
        } catch (e) {
            messageContext.push("Error", "Unknown error", MESSAGE_TYPES.ERROR);
        }

        setProcessing(false);
    };

    const handleUpload = () => async (evt) => {
        setProcessing(true);
        try {
            var formData = new FormData();
            formData.append("tallySheetId", tallySheetId);
            formData.append("scannedFile", evt.target.files[0]);
            const proofStatus = await tallySheetContext.uploadTallySheetProof(formData);
            messageContext.push("Success", MESSAGES_EN.success_upload, MESSAGE_TYPES.SUCCESS);
        } catch (e) {
            messageContext.push("Error", MESSAGES_EN.error_upload, MESSAGE_TYPES.ERROR);
        }
        setProcessing(false);
    };

    function getFileIcon({fileMimeType}) {
        if (/^image\/.*/.test(fileMimeType)) {
            return <ImageIcon/>
        } else if (/pdf/.test(fileMimeType)) {
            return <PictureAsPdfIcon/>
        } else {
            return <DescriptionIcon/>
        }
    }

    return <Dialog open={open} onClose={handleClose()} maxWidth="md" fullWidth={true}>
        <div style={{display: "flex", flex: 0, padding: 15}}>
            <Typography variant="h5" style={{flex: 1}}>{title}</Typography>
            <IconButton aria-label="close" onClick={handleClose()}>
                <CloseIcon/>
            </IconButton>
        </div>
        {(() => {
            if (allowUpload) {
                return <div style={{flex: 0, padding: 10}}>
                    <Button
                        style={{width: "100%", height: 50, border: "2px dashed #c1c0c0"}}
                        variant="outlined" color="default" component="label" size="small">
                        Upload file
                        <input accept="image/*,application/pdf" type="file" style={{display: 'none'}}
                               onChange={handleUpload()}/>
                    </Button>
                </div>
            }
        })()}
        <DialogContent style={{minHeight: 200}}>
            <Processing showProgress={processing}/>
            <List>
                {files.map(({fileId, dataUrl, fileName, fileType, fileCreatedBy, fileCreatedAt, fileMimeType}) => {
                    return <ListItem key={fileId}>
                        <ListItemAvatar>
                            {getFileIcon({fileMimeType})}
                        </ListItemAvatar>
                        <ListItemText
                            primary={fileName}
                            secondary={`${fileCreatedAt} by ${fileCreatedBy}`}
                        />
                        <PreviewTallySheetProofFileButton tallySheetId={tallySheetId} fileId={fileId}>
                            View
                        </PreviewTallySheetProofFileButton>
                    </ListItem>
                })}
            </List>
        </DialogContent>
        <DialogActions>
            {actions.map(({value, onClick}, actionIndex) => {
                return <Button key={actionIndex} onClick={onClick()} color="default" variant="outlined">
                    {value}
                </Button>
            })}
        </DialogActions>
    </Dialog>
}
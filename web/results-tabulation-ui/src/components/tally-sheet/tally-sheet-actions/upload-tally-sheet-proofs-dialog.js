import React from "react";
import Slide from "@material-ui/core/Slide";
import Dialog from "@material-ui/core/Dialog";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions";

export function UploadTallySheetProofsDialog({open, handleClose, handleOk}) {
    const Transition = React.forwardRef(function Transition(props, ref) {
        return <Slide direction="up" ref={ref} {...props} />;
    });

    return <Dialog fullScreen open={open} onClose={handleClose()} TransitionComponent={Transition}>
        <AppBar style={{backgroundColor: "#009688"}}>
            <Toolbar>
                <IconButton edge="start" color="inherit" onClick={handleClose()}
                            aria-label="close">
                    <CloseIcon/>
                </IconButton>
                <Typography variant="h6" style={{flex: 1, marginLeft: 10}}>
                    Please upload signed documents and certify
                </Typography>
                {/*<Button autoFocus color="inherit" onClick={handleOk()}>*/}
                {/*    Certify*/}
                {/*</Button>*/}
            </Toolbar>
        </AppBar>
        <DialogContent style={{paddingTop: 70}}>
            <DialogContentText id="alert-dialog-slide-description">
                <strong>-- TBA --</strong>
            </DialogContentText>
        </DialogContent>
        <DialogActions>
            <Button onClick={handleClose()} color="default" variant="outlined">
                Cancel
            </Button>
            <Button onClick={handleOk()} color="default" variant="outlined">
                Certify
            </Button>
        </DialogActions>
    </Dialog>
}
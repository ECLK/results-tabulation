import React, {useState} from "react";
// import CustomizedSnackbars from "../components/snack-bar"
import CustomizedDialog from "../components/dialog"
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import Slide from "@material-ui/core/Slide";

const DialogContext = React.createContext([]);

export const DIALOG_TYPES = {
    SUCCESS: "success",
    ERROR: "error",
    INFO: "info",
    WARNING: "warning"
};

export function DialogProvider(props) {
    const [state, setState] = useState({
        dialogsList: [],
        dialogsMap: {}
    });

    const push = function (dialogTitle, dialogBody, dialogType = DIALOG_TYPES.INFO) {
        const dialog = {
            dialogId: state.dialogsList.length,
            dialogTitle, dialogBody, dialogType,
            open: true,
            actionPromise: new Promise((resolve, reject) => {
                dialog.actionPromiseResolve = resolve;
                dialog.actionPromiseReject = reject;
            })
        };

        setState({
            ...state,
            dialogsList: [
                ...state.dialogsList,
                dialog.dialogId
            ],
            dialogsMap: {
                ...state.dialogsMap,
                [dialog.dialogId]: dialog
            }
        });

        return dialog.actionPromise;
    };

    const closeMessage = function (dialogId) {
        setState({
            ...state,
            dialogsMap: {
                ...state.dialogsMap,
                [dialogId]: {
                    ...state.dialogsMap[dialogId],
                    open: false
                }
            }
        })
    };

    const handleCloseMessage = (dialogId) => (event) => {
        closeMessage(dialogId)
    };


    return <DialogContext.Provider
        value={{push, dialogs: state.dialogsList.map((dialogId) => state.dialogsMap[dialogId])}}
    >
        {state.dialogsList.map((dialogId) => {
            const dialog = state.dialogsMap[dialogId];
            if (dialog.open && dialogId === (state.dialogsList.length - 1)) {
                const Transition = React.forwardRef(function Transition(props, ref) {
                    return <Slide direction="up" ref={ref} {...props} />;
                });

                const handleClose = () => (event) => {
                    dialog.actionPromiseResolve(0);
                };

                const handleOk = () => (event) => {
                    dialog.actionPromiseResolve(1);
                };


                return <Dialog
                    key={dialogId}
                    open={true}
                    TransitionComponent={Transition}
                    keepMounted
                    onClose={handleClose}
                    aria-labelledby="alert-dialog-slide-title"
                    aria-describedby="alert-dialog-slide-description"
                >
                    <DialogTitle id="alert-dialog-slide-title">{"Use Google's location service?"}</DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-slide-description">
                            <strong>{dialog.dialogTitle}</strong>
                            <div>{dialog.dialogBody}</div>
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose} color="primary">
                            Cancel
                        </Button>
                        <Button onClick={handleClose} color="primary">
                            Ok
                        </Button>
                    </DialogActions>
                </Dialog>

            }
        })}
        {props.children}
    </DialogContext.Provider>
}

export const DialogConsumer = DialogContext.Consumer;

import React, {useState} from "react";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import Slide from "@material-ui/core/Slide";

import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import CloseIcon from '@material-ui/icons/Close';

export const DialogContext = React.createContext([]);

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

    function push({dialogTitle, dialogBody, dialogType = DIALOG_TYPES.INFO, render}) {
        const dialog = {
            dialogId: state.dialogsList.length,
            dialogTitle, dialogBody, dialogType,
            open: true,
            render
        };

        dialog.actionPromise = new Promise((resolve, reject) => {
            dialog.actionPromiseResolve = resolve;
            dialog.actionPromiseReject = reject;
        });

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
            if (dialog.open) {
                const handleClose = () => (event) => {
                    setState((prevState) => {
                        Object.assign(prevState.dialogsMap[dialogId], {open: false});

                        return {...prevState};
                    });
                };
                const handleOk = () => (event) => {
                    dialog.actionPromiseResolve();
                    handleClose()(event);
                };
                const dialogProps = {open: dialog.open, handleClose, handleOk};

                return dialog.render(dialogProps);
            }
        })}
        {props.children}
    </DialogContext.Provider>
}

export const DialogConsumer = DialogContext.Consumer;

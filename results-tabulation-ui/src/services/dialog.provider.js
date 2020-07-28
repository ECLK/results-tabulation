import React, {useState} from "react";

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
                const handleClose = (data = null) => (event) => {
                    setState((prevState) => {
                        Object.assign(prevState.dialogsMap[dialogId], {open: false});

                        return {...prevState};
                    });
                    dialog.actionPromiseResolve(data);
                };
                const handleOk = (data = null) => (event) => {
                    handleClose(data)(event);
                };
                const dialogProps = {key: dialogId, open: dialog.open, handleClose, handleOk};

                return dialog.render(dialogProps);
            }
        })}
        {props.children}
    </DialogContext.Provider>
}

export const DialogConsumer = DialogContext.Consumer;

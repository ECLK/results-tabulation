import React, {useState} from "react";
import CustomizedSnackbars from "../components/snack-bar"

export const MessagesContext = React.createContext([]);

export const MESSAGE_TYPES = {
    SUCCESS: "success",
    ERROR: "error",
    INFO: "info",
    WARNING: "warning"
};

export function MessagesProvider(props) {
    const [state, setState] = useState({
        messagesList: [],
        messagesMap: {}
    });

    const push = function ({messageTitle, messageBody, messageType = MESSAGE_TYPES.INFO}) {
        const message = {messageId: state.messagesList.length, messageTitle, messageBody, messageType, open: true};
        setState({
            ...state,
            messagesList: [
                ...state.messagesList,
                message.messageId
            ],
            messagesMap: {
                ...state.messagesMap,
                [message.messageId]: message
            }
        })
    };

    const closeMessage = function (messageId) {
        setState({
            ...state,
            messagesMap: {
                ...state.messagesMap,
                [messageId]: {
                    ...state.messagesMap[messageId],
                    open: false
                }
            }
        })
    };

    const handleCloseMessage = (messageId) => (event) => {
        closeMessage(messageId)
    };


    return <MessagesContext.Provider
        value={{push}}
    >
        {state.messagesList.map((messageId) => {
            const message = state.messagesMap[messageId];
            if (message.open && messageId === (state.messagesList.length - 1)) {
                return <CustomizedSnackbars key={messageId} title={message.messageTitle} type={message.messageType}
                                            content={message.messageBody}/>
            }
        })}
        {props.children}
    </MessagesContext.Provider>
}

export const MessagesConsumer = MessagesContext.Consumer;

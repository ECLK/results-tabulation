import React, {useContext, useState} from "react";
import {PATH_ELECTION_TALLY_SHEET_VIEW} from "../../../App";
import Button from "@material-ui/core/Button";
import {TallySheetContext} from "../../../services/tally-sheet.provider";
import {
    WORKFLOW_ACTION_TYPE_CERTIFY,
    WORKFLOW_ACTION_TYPE_EDIT,
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
    WORKFLOW_ACTION_TYPE_PRINT, WORKFLOW_ACTION_TYPE_PRINT_LETTER,
    WORKFLOW_ACTION_TYPE_RELEASE, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
    WORKFLOW_ACTION_TYPE_SAVE,
    WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT,
    WORKFLOW_ACTION_TYPE_VERIFY,
    WORKFLOW_ACTION_TYPE_VIEW
} from "../constants/WORKFLOW_ACTION_TYPE";
import {DialogContext} from "../../../services/dialog.provider";
import {UploadTallySheetProofsDialog} from "./upload-tally-sheet-proofs-dialog";
import {MESSAGE_TYPES, MessagesContext} from "../../../services/messages.provider";
import PrintLetterButton from "../print-letter-button";
import PrintReportButton from "../print-report-button";
import {getErrorCode, getErrorMessage} from "../../../utils";

const TALLY_SHEET_ACTION_SUCCESS_MESSAGE = {
    [WORKFLOW_ACTION_TYPE_SUBMIT]: "Submitted tally sheet successfully.",
    [WORKFLOW_ACTION_TYPE_VERIFY]: "Verified tally sheet successfully.",
    [WORKFLOW_ACTION_TYPE_CERTIFY]: "Certified tally sheet successfully.",
    [WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY]: "Moved the tally sheet for certifying.",
    [WORKFLOW_ACTION_TYPE_CERTIFY]: "Certified tally sheet successfully.",
    [WORKFLOW_ACTION_TYPE_RELEASE]: "Released tally sheet results successfully.",
    [WORKFLOW_ACTION_TYPE_REQUEST_CHANGES]: "Submitted change request.",
};

const WORKFLOW_ACTION_CUSTOM_ACTION_BUTTON_MAP = {
    [WORKFLOW_ACTION_TYPE_PRINT_LETTER]: PrintLetterButton,
    [WORKFLOW_ACTION_TYPE_PRINT]: PrintReportButton
}

export default function TallySheetActions({tallySheetId, electionId, history, filter}) {
    const tallySheetContext = useContext(TallySheetContext);
    const dialogContext = useContext(DialogContext);
    const messageContext = useContext(MessagesContext);

    const tallySheet = tallySheetContext.getTallySheetById(tallySheetId);
    const [processing, setProcessing] = useState(false);

    const fetchAndRefreshData = async () => {
        try {
            await tallySheetContext.fetchTallySheetById(tallySheetId);
        } catch (e) {
            const errorCode = getErrorCode(e);
            if (errorCode) {
                const messageTitle = "Unknown Error";
                const messageBody = getErrorMessage(errorCode);
                const messageType = MESSAGE_TYPES.ERROR;
                messageContext.push({messageTitle, messageBody, messageType})
            }
        }
    };

    const tallySheetActionsJsx = tallySheet.workflowInstance.actions.filter((action) => {
        if (action.allowed) {
            if (filter) {
                return filter(action);
            } else {
                return true;
            }
        } else {
            return false;
        }
    }).map((action, actionIndex) => {
        let ActionButtonElement = Button;

        const onClick = async () => {

            setProcessing(true);

            try {
                if ([
                    WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT
                ].indexOf(action.actionType) < 0) {
                    await tallySheetContext.executeTallySheetWorkflow(tallySheet.tallySheetId, action.workflowActionId, tallySheet.latestVersionId);
                }

                if ([
                    WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_EDIT, WORKFLOW_ACTION_TYPE_SAVE
                ].indexOf(action.actionType) >= 0) {
                    history.push(PATH_ELECTION_TALLY_SHEET_VIEW(tallySheet.tallySheetId))
                } else {
                    let messageTitle = TALLY_SHEET_ACTION_SUCCESS_MESSAGE[action.actionType];
                    let messageBody = messageTitle;
                    let messageType = MESSAGE_TYPES.SUCCESS;

                    // Trigger the success message only for those actions where a message is defined.
                    if (messageTitle) {
                        messageContext.push({messageTitle, messageBody, messageType})
                    }
                }
            } catch (e) {
                const errorCode = getErrorCode(e);
                if (errorCode) {
                    const messageTitle = "Unknown Error";
                    const messageBody = getErrorMessage(errorCode);
                    const messageType = MESSAGE_TYPES.ERROR;
                    messageContext.push({messageTitle, messageBody, messageType})
                }

                await fetchAndRefreshData();
            }

            setProcessing(false);
        };

        const actionButtonProps = {
            key: actionIndex,
            variant: "outlined",
            color: "primary",
            size: "small",
            disabled: processing || !action.authorized,
            onClick: async () => {
                setProcessing(true);

                if (action.actionType === WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT) {
                    await dialogContext.push({
                        render({open, handleClose, handleOk}) {
                            return <UploadTallySheetProofsDialog
                                allowUpload={true} title="Upload certified documents"
                                tallySheetId={tallySheetId} open={open} handleClose={handleClose} handleOk={handleOk}/>
                        }
                    })
                } else if (action.actionType === WORKFLOW_ACTION_TYPE_RELEASE) {
                    await dialogContext.push({
                        render({open, handleClose, handleOk}) {
                            return <UploadTallySheetProofsDialog
                                allowUpload={false} title="Release confirmation"
                                tallySheetId={tallySheetId} open={open} handleClose={handleClose} handleOk={handleOk}
                                actions={[
                                    {value: "Confirm and Release", onClick: handleOk},
                                    {value: "Cancel", onClick: handleClose}
                                ]}
                            />
                        }
                    });
                    await onClick();
                } else {
                    await onClick();
                }

                setProcessing(false);
            }
        };

        if (WORKFLOW_ACTION_CUSTOM_ACTION_BUTTON_MAP[action.actionType]) {
            ActionButtonElement = WORKFLOW_ACTION_CUSTOM_ACTION_BUTTON_MAP[action.actionType];
            Object.assign(actionButtonProps, {tallySheetId: tallySheet.tallySheetId});
        }

        return <ActionButtonElement {...actionButtonProps}>
            {action.actionName}
        </ActionButtonElement>
    });

    return tallySheetActionsJsx;
}

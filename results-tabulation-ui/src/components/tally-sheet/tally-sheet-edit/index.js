import React, {useEffect, useState, Component, useContext} from "react";
import {MESSAGES_EN} from "../../../locale/messages_en";
import {MESSAGE_TYPES, MessagesContext} from "../../../services/messages.provider";
import {
    TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_CE_201_PV
} from "../constants/TALLY_SHEET_CODE";
import TallySheetEdit_CE_201 from "./tally-sheet-edit-ce-201";
import TallySheetEdit_CE_201_PV from "./tally-sheet-edit-ce-201-pv";
import {TallySheetContext} from "../../../services/tally-sheet.provider";
import TallySheetActions from "../tally-sheet-actions";
import Button from "@material-ui/core/Button";
import {getErrorCode, getErrorMessage} from "../../../utils";


export default class TallySheetEdit extends Component {
    getTallySheetEditForm(tallySheetCode) {
        if (tallySheetCode === TALLY_SHEET_CODE_CE_201) {
            return TallySheetEdit_CE_201;
        } else if (tallySheetCode === TALLY_SHEET_CODE_CE_201_PV) {
            return TallySheetEdit_CE_201_PV;
        } else {
            return null
        }
    }

    render() {
        const {tallySheet} = this.props;
        const {tallySheetCode} = tallySheet;
        const TallySheetEditComponent = this.getTallySheetEditForm(tallySheetCode);

        if (TallySheetEditComponent) {
            return <TallySheetEditComponent {...this.props} />
        } else {
            return <div>
                Tally sheet edit form has not been implemented yet.
            </div>;
        }
    }
}


export function useTallySheetEdit(props) {
    const tallySheetContext = useContext(TallySheetContext);
    const messagesContext = useContext(MessagesContext);

    const {history, election, setTallySheetContent, validateTallySheetContent, getTallySheetRequestBody} = props;
    const [processing, setProcessing] = useState(true);
    const [tallySheetVersion, setTallySheetVersion] = useState(null);
    const [processingLabel, setProcessingLabel] = useState("Loading");
    const [saved, setSaved] = useState(false);

    const {tallySheet} = props;
    const {tallySheetId, tallySheetCode} = tallySheet;
    const {electionId} = election;

    const init = async () => {
        setProcessing(true);
        if (tallySheet.latestVersion) {
            try {
                // const tallySheetVersion = await tabulationApi.getTallySheetVersionById(tallySheetId, tallySheetCode, tallySheet.latestVersionId);
                await setTallySheetContent(tallySheet.latestVersion);
                setProcessing(false);
            } catch (error) {
                messagesContext.push({
                    messageTitle: "Error",
                    messageBody: MESSAGES_EN.error_tallysheet_not_reachable,
                    messageType: MESSAGE_TYPES.ERROR
                });
                setProcessing(false);
            }
        } else {
            setTallySheetContent(tallySheetVersion);
            setProcessing(false);
        }
    };

    useEffect(() => {
        init();
    }, []);
    
    const handleClickNext = () => async (event) => {
        const body = getTallySheetRequestBody();

        if (validateTallySheetContent()) {
            setProcessing(true);
            setProcessingLabel("Saving");
            try {
                const tallySheet = await tallySheetContext.saveTallySheetVersion(tallySheetId, tallySheetCode, body);
                setTallySheetVersion(tallySheet.latestVersion);
                setSaved(true);
            } catch (e) {
                const errorCode = getErrorCode(e);
                messagesContext.push({
                    messageTitle: "Error",
                    messageBody: getErrorMessage(errorCode),
                    messageType: MESSAGE_TYPES.ERROR
                });
            }
            setProcessing(false);
        } else {
            messagesContext.push({
                messageTitle: "Error",
                messageBody: MESSAGES_EN.error_input,
                messageType: MESSAGE_TYPES.ERROR
            });
        }
    };

    const getActionsBar = () => {
        if (saved) {
            return <div className="page-bottom-fixed-action-bar">
                <TallySheetActions
                    tallySheetId={tallySheet.tallySheetId}
                    electionId={electionId} history={history}
                    // onTallySheetUpdate={setTallySheet}
                />
            </div>
        } else if (!processing) {
            return <div className="page-bottom-fixed-action-bar">
                <Button
                    variant="outlined" color="primary" onClick={handleClickNext()}
                    disabled={processing}
                >
                    Save & Next
                </Button>
            </div>
        } else {
            return null;
        }
    };

    return {tallySheet, tallySheetVersion, processing, processingLabel, saved, getActionsBar};
}


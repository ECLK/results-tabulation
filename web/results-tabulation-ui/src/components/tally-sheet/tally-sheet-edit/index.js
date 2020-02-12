import React, {useEffect, useState, Component} from "react";
import * as tabulationApi from "../../../services/tabulation-api";
import {MESSAGES_EN} from "../../../locale/messages_en";
import {MESSAGE_TYPES} from "../../../services/messages.provider";
import {PATH_ELECTION_TALLY_SHEET_LIST} from "../../../App";
import {
    TALLY_SHEET_CODE_CE_201
} from "../constants/TALLY_SHEET_CODE";
import TallySheetEdit_CE_201 from "./tally-sheet-edit-ce-201";


export default class TallySheetEdit extends Component {
    getTallySheetEditForm(tallySheetCode) {debugger;
        if (tallySheetCode === TALLY_SHEET_CODE_CE_201) {
            return TallySheetEdit_CE_201;
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
    const {messages, history, election, setTallySheetContent, validateTallySheetContent, getTallySheetRequestBody} = props;
    const [processing, setProcessing] = useState(true);
    const [tallySheetVersion, setTallySheetVersion] = useState(null);
    const [tallySheet, setTallySheet] = useState(props.tallySheet);
    const [processingLabel, setProcessingLabel] = useState("Loading");
    const [saved, setSaved] = useState(false);

    const {tallySheetId, tallySheetCode} = tallySheet;
    const {electionId} = election;

    useEffect(() => {
        setProcessing(true);
        if (tallySheet.latestVersionId) {
            tabulationApi.getTallySheetVersionById(tallySheetId, tallySheetCode, tallySheet.latestVersionId).then((tallySheetVersion) => {
                setTallySheetContent(tallySheetVersion);
                setProcessing(false);
            }).catch((error) => {
                debugger;
                messages.push("Error", MESSAGES_EN.error_tallysheet_not_reachable, MESSAGE_TYPES.ERROR);
                setProcessing(false);
            })
        } else {
            setTallySheetContent(tallySheetVersion);
            setProcessing(false);
        }
    }, []);

    const handleClickBackToEdit = (body) => async (event) => {
        setSaved(false);
    };

    const handleClickNext = () => async (event) => {
        const body = getTallySheetRequestBody();

        if (validateTallySheetContent()) {
            setSaved(true);
            setProcessing(true);
            setProcessingLabel("Saving");
            try {
                const tallySheetVersion = await tabulationApi.saveTallySheetVersion(tallySheetId, tallySheetCode, body);
                setTallySheetVersion(tallySheetVersion);
            } catch (e) {
                messages.push("Error", MESSAGES_EN.error_tallysheet_save, MESSAGE_TYPES.ERROR);
            }
            setProcessing(false);
        } else {
            messages.push("Error", MESSAGES_EN.error_input, MESSAGE_TYPES.ERROR)
        }
    };

    const handleClickSubmit = () => async (event) => {
        setProcessing(true);
        setProcessingLabel("Submitting");
        try {
            const {tallySheetVersionId} = tallySheetVersion;
            const tallySheet = await tabulationApi.submitTallySheet(tallySheetId, tallySheetVersionId);
            setTallySheet(tallySheet);

            messages.push("Success", MESSAGES_EN.success_pre41_submit, MESSAGE_TYPES.SUCCESS);
            setTimeout(() => {
                history.push(PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode));
            }, 1000)
        } catch (e) {
            messages.push("Error", MESSAGES_EN.error_tallysheet_submit, MESSAGE_TYPES.ERROR);
        }

        setProcessing(false);
    };

    return {
        tallySheet, tallySheetVersion, processing, processingLabel, saved,
        handleClickNext,
        handleClickSubmit,
        handleClickBackToEdit
    };
}


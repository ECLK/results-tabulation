import React, {Component, useEffect, useState} from "react";

import {
    PATH_ELECTION, PATH_ELECTION_BY_ID,
    PATH_ELECTION_DATA_ENTRY, PATH_ELECTION_DATA_ENTRY_EDIT,
    TALLY_SHEET_CODE_CE_201, TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_41, TALLY_SHEET_CODE_PRE_34_CO
} from "../../App";
import BreadCrumb from "../../components/bread-crumb";
import DataEntryEdit_PRE_41 from "./data-entry-edit-pre-41";
import DataEntryEdit_CE_201 from "./data-entry-edit-ce-201";
import DataEntryEdit_CE_201_PV from "./data-entry-edit-ce-201-pv";
import DataEntryEdit_PRE_34_CO from "./data-entry-edit-pre-34-co";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import * as tabulationApi from "../../services/tabulation-api";
import {MESSAGES_EN} from "../../locale/messages_en";
import {MESSAGE_TYPES} from "../../services/messages.provider";


export default function DataEntryEdit({history, queryString, election, tallySheet, messages}) {
    const {tallySheetId, tallySheetCode} = tallySheet;
    const subElectionId = tallySheet.electionId;
    const {electionId, electionName} = election;

    function getEditorJsx() {
        const props = {history, queryString, election, tallySheet, messages};
        if (tallySheetCode === TALLY_SHEET_CODE_PRE_41) {
            return <DataEntryEdit_PRE_41 {...props} />
        } else if (tallySheetCode === TALLY_SHEET_CODE_CE_201) {
            return <DataEntryEdit_CE_201 {...props} />
        } else if (tallySheetCode === TALLY_SHEET_CODE_CE_201_PV) {
            return <DataEntryEdit_CE_201_PV {...props} />
        } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_34_CO) {
            return <DataEntryEdit_PRE_34_CO {...props} />
        } else {
            return null;
        }
    }

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: electionName, to: PATH_ELECTION_BY_ID(electionId)},
                {
                    label: getTallySheetCodeStr(tallySheet).toLowerCase(),
                    to: PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId)
                },
                {
                    label: tallySheet.area.areaName,
                    to: PATH_ELECTION_DATA_ENTRY_EDIT(electionId, tallySheet.tallySheetId)
                },
            ]}
        />
        <div className="page-content">
            <div className="data-entry-edit-header">
                <div className="data-entry-edit-header-election-name">{electionName}</div>
                <div className="data-entry-edit-header-tally-sheet-code">{getTallySheetCodeStr(tallySheet)}</div>
            </div>
            <div>{tallySheet.electoralDistrict ? 'Electoral District: ' + tallySheet.electoralDistrict.areaName : null}
                {tallySheet.pollingDivision ? ' > Polling Division: ' + tallySheet.pollingDivision.areaName : null}
                {tallySheet.countingCentre ? ' > Counting Centre: ' + tallySheet.countingCentre.areaName : null}</div>
            {getEditorJsx()}
        </div>
    </div>
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
                const subElectionId = tallySheet.electionId;
                history.push(PATH_ELECTION_DATA_ENTRY(electionId, tallySheetCode, subElectionId));
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


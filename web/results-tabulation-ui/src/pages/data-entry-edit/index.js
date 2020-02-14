import React, {useEffect, useState} from "react";
import {
    PATH_ELECTION, PATH_ELECTION_BY_ID,
    PATH_ELECTION_TALLY_SHEET_LIST, PATH_ELECTION_TALLY_SHEET_VIEW
} from "../../App";
import BreadCrumb from "../../components/bread-crumb";
import {getTallySheetCodeStr} from "../../utils/tallySheet";
import * as tabulationApi from "../../services/tabulation-api";
import {MESSAGES_EN} from "../../locale/messages_en";
import {MESSAGE_TYPES} from "../../services/messages.provider";
import ExtendedElection from "../../components/election/extended-election";


export default function DataEntryEdit({history, queryString, election, tallySheet, messages}) {
    const {tallySheetCode} = tallySheet;
    const {electionId, rootElection} = election;

    function getEditorJsx() {
        const props = {history, queryString, election, tallySheet, messages};
        const extendedElection = ExtendedElection(election);

        return <extendedElection.TallySheetEditComponent {...props}/>
    }

    return <div className="page">
        <BreadCrumb
            links={[
                {label: "elections", to: PATH_ELECTION()},
                {label: rootElection.electionName, to: PATH_ELECTION_BY_ID(rootElection.electionId)},
                {
                    label: getTallySheetCodeStr(tallySheet).toLowerCase(),
                    to: PATH_ELECTION_TALLY_SHEET_LIST(electionId, tallySheetCode)
                },
                {
                    label: tallySheet.area.areaName,
                    to: PATH_ELECTION_TALLY_SHEET_VIEW(electionId, tallySheet.tallySheetId)
                },
            ]}
        />
        <div className="page-content">
            <div className="data-entry-edit-header">
                <div className="data-entry-edit-header-election-name">{rootElection.electionName}</div>
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


import React, {useState} from "react";
import ExtendedElection from "../components/election/extended-election";
import {
    ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML,
    ENDPOINT_PATH_TALLY_SHEET_WORKFLOW,
    ENDPOINT_PATH_TALLY_SHEETS,
    ENDPOINT_PATH_TALLY_SHEETS_BY_ID,
    request
} from "./tabulation-api";
import {ElectionEntity} from "./tabulation-api/entities/election.entity";

export const TallySheetContext = React.createContext([]);


const electionEntity = new ElectionEntity();

export function TallySheetProvider(props) {
    const [state, setState] = useState({
        tallySheetMap: {}
    });

    async function refactorTallySheetObject(tallySheet) {
        tallySheet.tallySheetCode = tallySheet.tallySheetCode.replace(/_/g, "-");
        tallySheet.election = await electionEntity.getById(tallySheet.electionId);

        tallySheet.metaDataMap = {};
        for (let i = 0; i < tallySheet.metaDataList.length; i++) {
            const {metaDataKey, metaDataValue} = tallySheet.metaDataList[i];
            tallySheet.metaDataMap[metaDataKey] = metaDataValue;
        }

        const extendedElection = ExtendedElection(tallySheet.election);
        tallySheet = await extendedElection.mapRequiredAreasToTallySheet(tallySheet);

        return tallySheet
    }

    async function getTallySheet({electionId, areaId, tallySheetCode, voteType, limit = 10000, offset = 0}) {
        const tallySheets = await request({
            url: ENDPOINT_PATH_TALLY_SHEETS(),
            method: 'get',
            params: {electionId, areaId, tallySheetCode, voteType, limit, offset}
        });

        const _tallySheetMap = {};
        for (let i = 0; i < tallySheets.length; i++) {
            const tallySheet = tallySheets[i];
            _tallySheetMap[tallySheet.tallySheetId] = tallySheet;
            await refactorTallySheetObject(tallySheet);
        }

        setState((state) => {
            return {
                ...state, tallySheetMap: {
                    ...state.tallySheetMap, ..._tallySheetMap
                }
            }
        });

        return tallySheets;
    }

    function _updateTallySheetState(tallySheet) {
        setState((state) => {
            return {
                ...state, tallySheetMap: {
                    ...state.tallySheetMap,
                    [tallySheet.tallySheetId]: {
                        ...state.tallySheetMap[tallySheet.tallySheetId],
                        ...tallySheet
                    }
                }
            }
        });
    }

    function getTallySheetById(tallySheetId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEETS_BY_ID(tallySheetId),
            method: 'get',
            params: {}
        }).then((tallySheet) => {
            _updateTallySheetState(tallySheet);
            return refactorTallySheetObject(tallySheet);
        })
    }

    function getById(tallySheetId) {
        return state.tallySheetMap[tallySheetId];
    }

    function getTallySheetVersionById(tallySheetId, tallySheetCode, tallySheetVersionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode, tallySheetVersionId),
            method: 'get',
            params: {}
        })
    }

    function uploadTallySheetProof(formData, onUploadProgress) {
        return request({
            url: `/proof/upload`,
            method: 'put',
            data: formData,
            onUploadProgress
        });
    }

    function executeTallySheetWorkflow(tallySheetId, workflowActionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_WORKFLOW(tallySheetId),
            method: 'put',
            data: {workflowActionId}
        }).then((tallySheet) => {
            _updateTallySheetState(tallySheet);
            return refactorTallySheetObject(tallySheet);
        })
    }

    function getTallySheetVersionHtml(tallySheetId, tallySheetVersionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML(tallySheetId, tallySheetVersionId),
            method: 'get'
        })
    }

    function getTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML(tallySheetId, tallySheetVersionId),
            method: 'get'
        })
    }

    function saveTallySheetVersion(tallySheetId, tallySheetCode, body = {}) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode),
            method: 'post',
            data: body
        })
    }

    function generateReport(tallySheetId, tallySheetVersionId) {
        return saveTallySheetVersion(tallySheetId, tallySheetVersionId)
    }

    return <TallySheetContext.Provider
        value={{
            getTallySheet,
            getTallySheetById,
            getTallySheetVersionById,
            uploadTallySheetProof,
            executeTallySheetWorkflow,
            getTallySheetVersionHtml,
            getTallySheetVersionLetterHtml,
            saveTallySheetVersion,
            getById
        }}
    >
        {props.children}
    </TallySheetContext.Provider>
}

export const TallySheetConsumer = TallySheetContext.Consumer;

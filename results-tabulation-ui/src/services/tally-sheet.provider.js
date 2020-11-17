import React, {useContext, useState} from "react";
import ExtendedElection from "../components/election/extended-election";
import {
    ENDPOINT_PATH_FILE, ENDPOINT_PATH_FILE_DOWNLOAD,
    ENDPOINT_PATH_TALLY_SHEET_PROOF,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML, ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_PDF,
    ENDPOINT_PATH_TALLY_SHEET_VERSION_PDF,
    ENDPOINT_PATH_TALLY_SHEET_WORKFLOW, ENDPOINT_PATH_TALLY_SHEET_WORKFLOW_LOGS,
    ENDPOINT_PATH_TALLY_SHEETS,
    ENDPOINT_PATH_TALLY_SHEETS_BY_ID,
    request
} from "./tabulation-api";
import {getMetaDataMap} from "./util";
import {ElectionContext} from "./election.provider";
import {TABULATION_API_PAGINATION_LIMIT} from "../config";

export const TallySheetContext = React.createContext([]);


export function TallySheetProvider(props) {
    const electionContext = useContext(ElectionContext);

    const [state, setState] = useState({
        tallySheetMap: {},
        tallySheetProofFileMap: {},
        filteredAreaMap: {}
    });

    async function getFilteredAreaMap(tallySheet) {
        const {areaId} = tallySheet;
        if (!state.filteredAreaMap[areaId]) {
            const electionAreaMap = await electionContext.getElectionAreaMap(tallySheet.electionId);
            state.filteredAreaMap[areaId] = electionAreaMap.filter((areaMap) => {
                return areaMap["countryId"] === areaId || areaMap["provinceId"] === areaId || areaMap["administrativeDistrictId"] === areaId || areaMap["electoralDistrictId"] === areaId || areaMap["pollingDivisionId"] === areaId || areaMap["countingCentreId"] === areaId || areaMap["countryId"] === areaId;
            });
            setState({
                ...state,
                filteredAreaMap: {
                    ...state.filteredAreaMap
                }
            })
        }

        return state.filteredAreaMap[areaId];
    }

    async function refactorTallySheetObject(tallySheet) {
        tallySheet.tallySheetCode = tallySheet.tallySheetCode.replace(/_/g, "-");
        tallySheet.election = await electionContext.getElectionById(tallySheet.electionId);
        tallySheet.areaMapList = await getFilteredAreaMap(tallySheet);

        // TODO fetch actions and area maps

        const {metaDataList = []} = tallySheet;
        tallySheet.metaDataMap = getMetaDataMap(metaDataList);

        const extendedElection = ExtendedElection(tallySheet.election);
        tallySheet = await extendedElection.mapRequiredAreasToTallySheet(tallySheet);

        return tallySheet
    }

    async function fetchTallySheetChunks({electionId, areaId, tallySheetCode, voteType, partyId}, next) {
        const limit = TABULATION_API_PAGINATION_LIMIT;
        let offset = 0;
        let reachedEnd = false;
        while (!reachedEnd) {
            const tallySheetIds = await fetchTallySheet({
                electionId,
                areaId,
                tallySheetCode,
                voteType,
                partyId,
                limit,
                offset: offset * limit
            });
            next && next(tallySheetIds);

            if (tallySheetIds.length < limit) {
                // Reached the end of the results.
                reachedEnd = true;
            }

            offset++;
        }
    }

    async function fetchTallySheet({electionId, areaId, tallySheetCode, voteType, partyId, limit = 10000, offset = 0}) {
        const tallySheets = await request({
            url: ENDPOINT_PATH_TALLY_SHEETS(),
            method: 'get',
            params: {electionId, areaId, tallySheetCode, voteType, partyId, limit, offset}
        });

        // const _tallySheetMap = {};
        const tallySheetIds = [];
        for (let i = 0; i < tallySheets.length; i++) {
            const tallySheet = tallySheets[i];
            const {tallySheetId} = tallySheet;
            tallySheetIds.push(tallySheetId);
            state.tallySheetMap[tallySheet.tallySheetId] = tallySheet;
            await refactorTallySheetObject(tallySheet);
            _updateTallySheetState(tallySheet)
        }

        return tallySheetIds;
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

    function fetchTallySheetById(tallySheetId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEETS_BY_ID(tallySheetId),
            method: 'get',
            params: {}
        }).then(async (tallySheet) => {
            tallySheet = await refactorTallySheetObject(tallySheet);
            _updateTallySheetState(tallySheet);
            return tallySheet;
        })
    }

    function getTallySheetById(tallySheetId) {
        return state.tallySheetMap[tallySheetId];
    }

    function fetchTallySheetVersionById(tallySheetId, tallySheetCode, tallySheetVersionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode, tallySheetVersionId),
            method: 'get',
            params: {}
        })
    }

    function uploadTallySheetProof(formData, onUploadProgress) {
        return request({
            url: `/tally-sheet/workflow/proof/upload`,
            method: 'put',
            data: formData,
            onUploadProgress
        }).then((tallySheet) => {
            _updateTallySheetState(tallySheet);
            return refactorTallySheetObject(tallySheet);
        });
    }

    function executeTallySheetWorkflow(tallySheetId, workflowActionId, tallySheetVersionId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_WORKFLOW(tallySheetId),
            method: 'put',
            data: {workflowActionId, tallySheetVersionId}
        }).then((tallySheet) => {
            _updateTallySheetState(tallySheet);
            return refactorTallySheetObject(tallySheet);
        })
    }

    function fetchTallySheetVersionHtml(tallySheetId, tallySheetVersionId = null) {
        if (!tallySheetVersionId) {
            tallySheetVersionId = state.tallySheetMap[tallySheetId].latestVersionId
        }

        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML(tallySheetId, tallySheetVersionId),
            method: 'post'
        })
    }

    function fetchTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId = null, signatures = []) {
        if (!tallySheetVersionId) {
            tallySheetVersionId = state.tallySheetMap[tallySheetId].latestVersionId
        }

        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML(tallySheetId, tallySheetVersionId),
            method: 'post',
            data: {signatures}
        })
    }

    function saveTallySheetVersion(tallySheetId, tallySheetCode, body = {}) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode),
            method: 'post',
            data: body
        }).then((tallySheet) => {
            _updateTallySheetState(tallySheet);
            return refactorTallySheetObject(tallySheet);
        })
    }

    function generateReport(tallySheetId, tallySheetVersionId) {
        return saveTallySheetVersion(tallySheetId, tallySheetVersionId)
    }

    function getTallySheetProof(tallySheetId, fileId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_PROOF(tallySheetId, fileId),
            method: 'get'
        });
    }

    async function getTallySheetProofFile(tallySheetId, fileId) {
        let file = state.tallySheetProofFileMap[fileId];
        if (!file) {
            file = await request({
                url: ENDPOINT_PATH_FILE(tallySheetId, fileId),
                method: 'get'
            }).then(_file => {
                setState(prevState => {
                    return {
                        ...prevState,
                        tallySheetProofFileMap: {...prevState.tallySheetProofFileMap, [fileId]: _file}
                    };
                });
                return _file;
            });
        }

        return file;
    }

    async function fetchTallySheetVersionPdfDataUrl(tallySheetId, tallySheetVersionId = null) {
        if (!tallySheetVersionId) {
            tallySheetVersionId = state.tallySheetMap[tallySheetId].latestVersionId
        }

        const fileArrayBuffer = await request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_PDF(tallySheetId, tallySheetVersionId),
            method: 'post',
            responseType: 'arraybuffer'
        });

        const fileBlob = new Blob([fileArrayBuffer], {type: "application/pdf"});
        const dataUrl = URL.createObjectURL(fileBlob);

        return dataUrl
    }

    async function fetchTallySheetVersionLetterPdfDataUrl(tallySheetId, tallySheetVersionId = null, signatures = []) {
        if (!tallySheetVersionId) {
            tallySheetVersionId = state.tallySheetMap[tallySheetId].latestVersionId
        }

        const fileArrayBuffer = await request({
            url: ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_PDF(tallySheetId, tallySheetVersionId),
            method: 'post',
            responseType: 'arraybuffer',
            data: {signatures}
        });

        const fileBlob = new Blob([fileArrayBuffer], {type: "application/pdf"});
        const dataUrl = URL.createObjectURL(fileBlob);

        return dataUrl
    }

    async function getTallySheetProofFileDataUrl(tallySheetId, fileId) {
        let file = await getTallySheetProofFile(tallySheetId, fileId);
        if (!file.dataUrl) {
            const fileArrayBuffer = await request({
                url: ENDPOINT_PATH_FILE_DOWNLOAD(tallySheetId, fileId),
                method: 'get',
                responseType: 'arraybuffer'
            });
            const fileBlob = new Blob([fileArrayBuffer], {type: file.fileMimeType});
            const dataUrl = URL.createObjectURL(fileBlob);
            file.dataUrl = dataUrl;
            setState(prevState => {
                return {
                    ...prevState, tallySheetProofFileMap: {
                        ...prevState.tallySheetProofFileMap,
                        [fileId]: {...prevState.tallySheetProofFileMap[fileId], dataUrl}
                    }
                };
            });
        }

        return file;
    }

    async function getTallySheetWorkflowLogList(tallySheetId) {
        return request({
            url: ENDPOINT_PATH_TALLY_SHEET_WORKFLOW_LOGS(tallySheetId),
            method: 'get'
        }).then(logs => {
            for (let i = 0; i < logs.length; i++) {
                const log = logs[i];
                const {metaDataList = []} = log;
                log.metaDataMap = getMetaDataMap(metaDataList);
            }

            return logs;
        })
    }

    return <TallySheetContext.Provider
        value={{
            fetchTallySheet,
            fetchTallySheetChunks,
            fetchTallySheetById,
            fetchTallySheetVersionById,
            uploadTallySheetProof,
            executeTallySheetWorkflow,
            fetchTallySheetVersionHtml,
            fetchTallySheetVersionLetterHtml,
            fetchTallySheetVersionPdfDataUrl,
            fetchTallySheetVersionLetterPdfDataUrl,
            saveTallySheetVersion,
            getTallySheetById,
            getTallySheetProofFile,
            getTallySheetProofFileDataUrl,
            getTallySheetWorkflowLogList
        }}
    >
        {props.children}
    </TallySheetContext.Provider>
}

export const TallySheetConsumer = TallySheetContext.Consumer;

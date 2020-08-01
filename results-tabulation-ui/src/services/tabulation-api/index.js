import axios from 'axios';
import {TABULATION_API_URL} from "../../config";
import {getAccessToken} from "../../auth";

export const ENDPOINT_PATH_ELECTIONS = () => "/election";
export const ENDPOINT_PATH_ELECTIONS_BY_ID = (electionId) => `/election/${electionId}`;
export const ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID = (electionId) => `/election/${electionId}/area-map`;
export const ENDPOINT_PATH_AREAS = () => "/area";
export const ENDPOINT_PATH_AREAS_BY_ID = (areaId) => `/area/${areaId}`;
export const ENDPOINT_PATH_TALLY_SHEETS = () => "/tally-sheet";
export const ENDPOINT_PATH_TALLY_SHEETS_BY_ID = (tallySheetId) => `/tally-sheet/${tallySheetId}`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID = (tallySheetId, tallySheetCode, tallySheetVersionId) => {
    let path = `/tally-sheet/${tallySheetId}/version`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`;
    }

    return path;
};
export const ENDPOINT_PATH_TALLY_SHEET_WORKFLOW = (tallySheetId) => `/tally-sheet/${tallySheetId}/workflow`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/html`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_PDF = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/pdf`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/letter/html`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_PDF = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/letter/pdf`;

export const ENDPOINT_PATH_TALLY_SHEET_PROOF = (tallySheetId, proofId) => `/tally-sheet/${tallySheetId}/workflow/proof/${proofId}`;
export const ENDPOINT_PATH_TALLY_SHEET_WORKFLOW_LOGS = (tallySheetId) => `/tally-sheet/${tallySheetId}/workflow/logs`;
export const ENDPOINT_PATH_TALLY_SHEET_PROOF_FINISH = (proofId) => `/proof/${proofId}/finish`;
export const ENDPOINT_PATH_FILE = (tallySheetId, fileId) => `/tally-sheet/${tallySheetId}/workflow/proof/file/${fileId}`;
export const ENDPOINT_PATH_FILE_DOWNLOAD = (tallySheetId, fileId) => `/tally-sheet/${tallySheetId}/workflow/proof/file/${fileId}/download`;


const axiosInstance = axios.create({
    baseURL: TABULATION_API_URL,
    headers: {
        'Authorization': "Bearer " + getAccessToken(),
        'X-Jwt-Assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3JvbGUiOlsidGFiX2FkbWluIiwidGFiX2RhdGFfZWRpdG9yIiwidGFiX3BvbF9kaXZfcmVwX3ZpZXciLCJ0YWJfcG9sX2Rpdl9yZXBfdmVyZiIsInRhYl9lbGNfZGlzX3JlcF92aWV3IiwidGFiX2VsY19kaXNfcmVwX3ZlcmYiLCJ0YWJfbmF0X2Rpc19yZXBfdmlldyIsInRhYl9uYXRfZGlzX3JlcF92ZXJmIiwidGFiX2VjX2xlYWRlcnNoaXAiXSwiaHR0cDovL3dzbzIub3JnL2NsYWltcy91c2VybmFtZSI6ImphbmFrQGNhcmJvbi5zdXBlciIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fYWRtaW4iOiJbXSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fZGF0YV9lZGl0b3IiOiJbeydhcmVhSWQnOiAzMDMwMywgJ2FyZWFOYW1lJzogJ0t1cnVuZWdhbGEnfSwgeydhcmVhSWQnOiAzMjI3NywgJ2FyZWFOYW1lJzogJ1BvbG9ubmFydXdhJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9wb2xfZGl2X3JlcF92aWV3IjoiW3snYXJlYUlkJzogMzAzMDMsICdhcmVhTmFtZSc6ICdLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMzIyNzcsICdhcmVhTmFtZSc6ICdQb2xvbm5hcnV3YSd9XSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fcG9sX2Rpdl9yZXBfdmVyZiI6Ilt7J2FyZWFJZCc6IDMwMzAzLCAnYXJlYU5hbWUnOiAnS3VydW5lZ2FsYSd9LCB7J2FyZWFJZCc6IDMyMjc3LCAnYXJlYU5hbWUnOiAnUG9sb25uYXJ1d2EnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAzMDMwMywgJ2FyZWFOYW1lJzogJ0t1cnVuZWdhbGEnfSwgeydhcmVhSWQnOiAzMjI3NywgJ2FyZWFOYW1lJzogJ1BvbG9ubmFydXdhJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9lbGNfZGlzX3JlcF92ZXJmIjoiW3snYXJlYUlkJzogMzAzMDMsICdhcmVhTmFtZSc6ICdLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMzIyNzcsICdhcmVhTmFtZSc6ICdQb2xvbm5hcnV3YSd9XSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fbmF0X2Rpc19yZXBfdmlldyI6Ilt7J2FyZWFJZCc6IDMwMzAyLCAnYXJlYU5hbWUnOiAnU3JpIExhbmthJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9uYXRfZGlzX3JlcF92ZXJmIjoiW3snYXJlYUlkJzogMzAzMDIsICdhcmVhTmFtZSc6ICdTcmkgTGFua2EnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VjX2xlYWRlcnNoaXAiOiJbeydhcmVhSWQnOiAzMDMwMiwgJ2FyZWFOYW1lJzogJ1NyaSBMYW5rYSd9XSJ9.CHNeG6qefaRb8rWFEW9tNltBZza2uXTw41rRFGH5YqA',
        // 'X-Jwt-Assertion': window.prompt("'X-Jwt-Assertion': "),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest'
    }
});

export function request(config) {
    return axiosInstance.request(config).then((res) => res.data)
}


export function getAreas({electionId, associatedAreaId, areaType, limit = 10000, offset = 0}) {
    return request({
        url: ENDPOINT_PATH_AREAS(),
        method: 'get', // default,
        params: {electionId, associatedAreaId, areaType, limit, offset}
    })
}






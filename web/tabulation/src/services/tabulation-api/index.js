import axios from 'axios';
import {TABULATION_API_URL} from "../../config";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD,
    TALLY_SHEET_CODE_PRE_41,
    TALLY_SHEET_CODE_PRE_34_CO,
    COUNTING_CENTRE_WISE_DATA_ENTRY_TALLY_SHEET_CODES,
    ALL_ISLAND_TALLY_SHEET_CODES,
    TALLY_SHEET_CODE_PRE_34_I_RO,
    TALLY_SHEET_CODE_PRE_34_II_RO,
    TALLY_SHEET_CODE_PRE_34,
    TALLY_SHEET_CODE_PRE_34_PD, TALLY_SHEET_CODE_PRE_34_ED
} from "../../App";
import {getAccessToken} from "../../auth";
import {AreaEntity} from "./entities/area.entity";
import {ElectionEntity, VOTE_TYPE} from "./entities/election.entity";
import {getFirstOrNull} from "../../utils";

export const ENDPOINT_PATH_ELECTIONS = () => "/election";
export const ENDPOINT_PATH_ELECTION_AREA = (electionId) => `/election/${electionId}/area`;
export const ENDPOINT_PATH_ELECTIONS_BY_ID = (electionId) => `/election/${electionId}`;
export const ENDPOINT_PATH_AREAS = () => "/area";
export const ENDPOINT_PATH_TALLY_SHEETS = () => "/tally-sheet";
export const ENDPOINT_PATH_TALLY_SHEETS_BY_ID = (tallySheetId) => `/tally-sheet/${tallySheetId}`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID = (tallySheetId, tallySheetCode, tallySheetVersionId) => {
    let path = `/tally-sheet/${tallySheetCode}/${tallySheetId}/version`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`;
    }

    return path;
};
export const ENDPOINT_PATH_TALLY_SHEET_LOCK = (tallySheetId) => `/tally-sheet/${tallySheetId}/lock`;
export const ENDPOINT_PATH_TALLY_SHEET_UNLOCK = (tallySheetId) => `/tally-sheet/${tallySheetId}/unlock`;
export const ENDPOINT_PATH_TALLY_SHEET_SUBMIT = (tallySheetId) => `/tally-sheet/${tallySheetId}/submit`;
export const ENDPOINT_PATH_TALLY_SHEET_REQUEST_EDIT = (tallySheetId) => `/tally-sheet/${tallySheetId}/request-edit`;
export const ENDPOINT_PATH_TALLY_SHEET_NOTIFY = (tallySheetId) => `/tally-sheet/${tallySheetId}/notify`;
export const ENDPOINT_PATH_TALLY_SHEET_RELEASE = (tallySheetId) => `/tally-sheet/${tallySheetId}/release`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/html`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/letter/html`;

export const ENDPOINT_PATH_TALLY_SHEET_PROOF = (proofId) => `/proof/${proofId}`;
export const ENDPOINT_PATH_TALLY_SHEET_PROOF_FINISH = (proofId) => `/proof/${proofId}/finish`;
export const ENDPOINT_PATH_FILE = (proofId) => `/file/${proofId}/download`;


const areaEntity = new AreaEntity();
const electionEntity = new ElectionEntity();

const axiosInstance = axios.create({
    baseURL: TABULATION_API_URL,
    headers: {
        'Authorization': "Bearer " + getAccessToken(),
        'X-Jwt-Assertion': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3JvbGUiOlsidGFiX2FkbWluIiwidGFiX2RhdGFfZWRpdG9yIiwidGFiX3BvbF9kaXZfcmVwX3ZpZXciLCJ0YWJfcG9sX2Rpdl9yZXBfdmVyZiIsInRhYl9lbGNfZGlzX3JlcF92aWV3IiwidGFiX2VsY19kaXNfcmVwX3ZlcmYiLCJ0YWJfbmF0X2Rpc19yZXBfdmlldyIsInRhYl9uYXRfZGlzX3JlcF92ZXJmIiwidGFiX2VjX2xlYWRlcnNoaXAiXSwiaHR0cDovL3dzbzIub3JnL2NsYWltcy91c2VybmFtZSI6ImphbmFrQGNhcmJvbi5zdXBlciIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fYWRtaW4iOiJbXSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fZGF0YV9lZGl0b3IiOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDEgLSBDb2xvbWJvJ30sIHsnYXJlYUlkJzogMjUwNywgJ2FyZWFOYW1lJzogJzAyIC0gR2FtcGFoYSd9LCB7J2FyZWFJZCc6IDUwMDIsICdhcmVhTmFtZSc6ICcwMyAtIEthbHV0YXJhJ30sIHsnYXJlYUlkJzogNjI2OCwgJ2FyZWFOYW1lJzogJzA0IC0gS2FuZHknfSwgeydhcmVhSWQnOiA4MDIyLCAnYXJlYU5hbWUnOiAnMDUgLSBNYXRhbGUnfSwgeydhcmVhSWQnOiA4NzA2LCAnYXJlYU5hbWUnOiAnMDYgLSBOdXdhcmEgRWxpeWEnfSwgeydhcmVhSWQnOiA5NzI1LCAnYXJlYU5hbWUnOiAnMDcgLSBHYWxsZSd9LCB7J2FyZWFJZCc6IDExMjM3LCAnYXJlYU5hbWUnOiAnMDggLSBNYXRhcmEnfSwgeydhcmVhSWQnOiAxMjE5OSwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9LCB7J2FyZWFJZCc6IDEzMDYxLCAnYXJlYU5hbWUnOiAnMTAgLSBKYWZmbmEnfSwgeydhcmVhSWQnOiAxNDM3NywgJ2FyZWFOYW1lJzogJzExIC0gVmFubmknfSwgeydhcmVhSWQnOiAxNTExNywgJ2FyZWFOYW1lJzogJzEyIC0gQmF0dGljYWxvYSd9LCB7J2FyZWFJZCc6IDE2MDA1LCAnYXJlYU5hbWUnOiAnMTMgLSBEaWdhbWFkdWxsYSd9LCB7J2FyZWFJZCc6IDE3MDk1LCAnYXJlYU5hbWUnOiAnMTQgLSBUcmluY29tYWxlZSd9LCB7J2FyZWFJZCc6IDE3NzM1LCAnYXJlYU5hbWUnOiAnMTUgLSBLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMTk3NjEsICdhcmVhTmFtZSc6ICcxNiAtIFB1dHRhbGFtJ30sIHsnYXJlYUlkJzogMjA2MTEsICdhcmVhTmFtZSc6ICcxNyAtIEFudXJhZGhhcHVyYSd9LCB7J2FyZWFJZCc6IDIxOTM0LCAnYXJlYU5hbWUnOiAnMTggLSBQb2xvbm5hcnV3YSd9LCB7J2FyZWFJZCc6IDIyNTQwLCAnYXJlYU5hbWUnOiAnMTkgLSBCYWR1bGxhJ30sIHsnYXJlYUlkJzogMjM2NDQsICdhcmVhTmFtZSc6ICcyMCAtIE1vbmFyYWdhbGEnfSwgeydhcmVhSWQnOiAyNDM4MywgJ2FyZWFOYW1lJzogJzIxIC0gUmF0bmFwdXJhJ30sIHsnYXJlYUlkJzogMjU3MDEsICdhcmVhTmFtZSc6ICcyMiAtIEtlZ2FsbGUnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDEgLSBDb2xvbWJvJ30sIHsnYXJlYUlkJzogMjUwNywgJ2FyZWFOYW1lJzogJzAyIC0gR2FtcGFoYSd9LCB7J2FyZWFJZCc6IDUwMDIsICdhcmVhTmFtZSc6ICcwMyAtIEthbHV0YXJhJ30sIHsnYXJlYUlkJzogNjI2OCwgJ2FyZWFOYW1lJzogJzA0IC0gS2FuZHknfSwgeydhcmVhSWQnOiA4MDIyLCAnYXJlYU5hbWUnOiAnMDUgLSBNYXRhbGUnfSwgeydhcmVhSWQnOiA4NzA2LCAnYXJlYU5hbWUnOiAnMDYgLSBOdXdhcmEgRWxpeWEnfSwgeydhcmVhSWQnOiA5NzI1LCAnYXJlYU5hbWUnOiAnMDcgLSBHYWxsZSd9LCB7J2FyZWFJZCc6IDExMjM3LCAnYXJlYU5hbWUnOiAnMDggLSBNYXRhcmEnfSwgeydhcmVhSWQnOiAxMjE5OSwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9LCB7J2FyZWFJZCc6IDEzMDYxLCAnYXJlYU5hbWUnOiAnMTAgLSBKYWZmbmEnfSwgeydhcmVhSWQnOiAxNDM3NywgJ2FyZWFOYW1lJzogJzExIC0gVmFubmknfSwgeydhcmVhSWQnOiAxNTExNywgJ2FyZWFOYW1lJzogJzEyIC0gQmF0dGljYWxvYSd9LCB7J2FyZWFJZCc6IDE2MDA1LCAnYXJlYU5hbWUnOiAnMTMgLSBEaWdhbWFkdWxsYSd9LCB7J2FyZWFJZCc6IDE3MDk1LCAnYXJlYU5hbWUnOiAnMTQgLSBUcmluY29tYWxlZSd9LCB7J2FyZWFJZCc6IDE3NzM1LCAnYXJlYU5hbWUnOiAnMTUgLSBLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMTk3NjEsICdhcmVhTmFtZSc6ICcxNiAtIFB1dHRhbGFtJ30sIHsnYXJlYUlkJzogMjA2MTEsICdhcmVhTmFtZSc6ICcxNyAtIEFudXJhZGhhcHVyYSd9LCB7J2FyZWFJZCc6IDIxOTM0LCAnYXJlYU5hbWUnOiAnMTggLSBQb2xvbm5hcnV3YSd9LCB7J2FyZWFJZCc6IDIyNTQwLCAnYXJlYU5hbWUnOiAnMTkgLSBCYWR1bGxhJ30sIHsnYXJlYUlkJzogMjM2NDQsICdhcmVhTmFtZSc6ICcyMCAtIE1vbmFyYWdhbGEnfSwgeydhcmVhSWQnOiAyNDM4MywgJ2FyZWFOYW1lJzogJzIxIC0gUmF0bmFwdXJhJ30sIHsnYXJlYUlkJzogMjU3MDEsICdhcmVhTmFtZSc6ICcyMiAtIEtlZ2FsbGUnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZlcmYiOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDEgLSBDb2xvbWJvJ30sIHsnYXJlYUlkJzogMjUwNywgJ2FyZWFOYW1lJzogJzAyIC0gR2FtcGFoYSd9LCB7J2FyZWFJZCc6IDUwMDIsICdhcmVhTmFtZSc6ICcwMyAtIEthbHV0YXJhJ30sIHsnYXJlYUlkJzogNjI2OCwgJ2FyZWFOYW1lJzogJzA0IC0gS2FuZHknfSwgeydhcmVhSWQnOiA4MDIyLCAnYXJlYU5hbWUnOiAnMDUgLSBNYXRhbGUnfSwgeydhcmVhSWQnOiA4NzA2LCAnYXJlYU5hbWUnOiAnMDYgLSBOdXdhcmEgRWxpeWEnfSwgeydhcmVhSWQnOiA5NzI1LCAnYXJlYU5hbWUnOiAnMDcgLSBHYWxsZSd9LCB7J2FyZWFJZCc6IDExMjM3LCAnYXJlYU5hbWUnOiAnMDggLSBNYXRhcmEnfSwgeydhcmVhSWQnOiAxMjE5OSwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9LCB7J2FyZWFJZCc6IDEzMDYxLCAnYXJlYU5hbWUnOiAnMTAgLSBKYWZmbmEnfSwgeydhcmVhSWQnOiAxNDM3NywgJ2FyZWFOYW1lJzogJzExIC0gVmFubmknfSwgeydhcmVhSWQnOiAxNTExNywgJ2FyZWFOYW1lJzogJzEyIC0gQmF0dGljYWxvYSd9LCB7J2FyZWFJZCc6IDE2MDA1LCAnYXJlYU5hbWUnOiAnMTMgLSBEaWdhbWFkdWxsYSd9LCB7J2FyZWFJZCc6IDE3MDk1LCAnYXJlYU5hbWUnOiAnMTQgLSBUcmluY29tYWxlZSd9LCB7J2FyZWFJZCc6IDE3NzM1LCAnYXJlYU5hbWUnOiAnMTUgLSBLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMTk3NjEsICdhcmVhTmFtZSc6ICcxNiAtIFB1dHRhbGFtJ30sIHsnYXJlYUlkJzogMjA2MTEsICdhcmVhTmFtZSc6ICcxNyAtIEFudXJhZGhhcHVyYSd9LCB7J2FyZWFJZCc6IDIxOTM0LCAnYXJlYU5hbWUnOiAnMTggLSBQb2xvbm5hcnV3YSd9LCB7J2FyZWFJZCc6IDIyNTQwLCAnYXJlYU5hbWUnOiAnMTkgLSBCYWR1bGxhJ30sIHsnYXJlYUlkJzogMjM2NDQsICdhcmVhTmFtZSc6ICcyMCAtIE1vbmFyYWdhbGEnfSwgeydhcmVhSWQnOiAyNDM4MywgJ2FyZWFOYW1lJzogJzIxIC0gUmF0bmFwdXJhJ30sIHsnYXJlYUlkJzogMjU3MDEsICdhcmVhTmFtZSc6ICcyMiAtIEtlZ2FsbGUnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDEgLSBDb2xvbWJvJ30sIHsnYXJlYUlkJzogMjUwNywgJ2FyZWFOYW1lJzogJzAyIC0gR2FtcGFoYSd9LCB7J2FyZWFJZCc6IDUwMDIsICdhcmVhTmFtZSc6ICcwMyAtIEthbHV0YXJhJ30sIHsnYXJlYUlkJzogNjI2OCwgJ2FyZWFOYW1lJzogJzA0IC0gS2FuZHknfSwgeydhcmVhSWQnOiA4MDIyLCAnYXJlYU5hbWUnOiAnMDUgLSBNYXRhbGUnfSwgeydhcmVhSWQnOiA4NzA2LCAnYXJlYU5hbWUnOiAnMDYgLSBOdXdhcmEgRWxpeWEnfSwgeydhcmVhSWQnOiA5NzI1LCAnYXJlYU5hbWUnOiAnMDcgLSBHYWxsZSd9LCB7J2FyZWFJZCc6IDExMjM3LCAnYXJlYU5hbWUnOiAnMDggLSBNYXRhcmEnfSwgeydhcmVhSWQnOiAxMjE5OSwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9LCB7J2FyZWFJZCc6IDEzMDYxLCAnYXJlYU5hbWUnOiAnMTAgLSBKYWZmbmEnfSwgeydhcmVhSWQnOiAxNDM3NywgJ2FyZWFOYW1lJzogJzExIC0gVmFubmknfSwgeydhcmVhSWQnOiAxNTExNywgJ2FyZWFOYW1lJzogJzEyIC0gQmF0dGljYWxvYSd9LCB7J2FyZWFJZCc6IDE2MDA1LCAnYXJlYU5hbWUnOiAnMTMgLSBEaWdhbWFkdWxsYSd9LCB7J2FyZWFJZCc6IDE3MDk1LCAnYXJlYU5hbWUnOiAnMTQgLSBUcmluY29tYWxlZSd9LCB7J2FyZWFJZCc6IDE3NzM1LCAnYXJlYU5hbWUnOiAnMTUgLSBLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMTk3NjEsICdhcmVhTmFtZSc6ICcxNiAtIFB1dHRhbGFtJ30sIHsnYXJlYUlkJzogMjA2MTEsICdhcmVhTmFtZSc6ICcxNyAtIEFudXJhZGhhcHVyYSd9LCB7J2FyZWFJZCc6IDIxOTM0LCAnYXJlYU5hbWUnOiAnMTggLSBQb2xvbm5hcnV3YSd9LCB7J2FyZWFJZCc6IDIyNTQwLCAnYXJlYU5hbWUnOiAnMTkgLSBCYWR1bGxhJ30sIHsnYXJlYUlkJzogMjM2NDQsICdhcmVhTmFtZSc6ICcyMCAtIE1vbmFyYWdhbGEnfSwgeydhcmVhSWQnOiAyNDM4MywgJ2FyZWFOYW1lJzogJzIxIC0gUmF0bmFwdXJhJ30sIHsnYXJlYUlkJzogMjU3MDEsICdhcmVhTmFtZSc6ICcyMiAtIEtlZ2FsbGUnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZlcmYiOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDEgLSBDb2xvbWJvJ30sIHsnYXJlYUlkJzogMjUwNywgJ2FyZWFOYW1lJzogJzAyIC0gR2FtcGFoYSd9LCB7J2FyZWFJZCc6IDUwMDIsICdhcmVhTmFtZSc6ICcwMyAtIEthbHV0YXJhJ30sIHsnYXJlYUlkJzogNjI2OCwgJ2FyZWFOYW1lJzogJzA0IC0gS2FuZHknfSwgeydhcmVhSWQnOiA4MDIyLCAnYXJlYU5hbWUnOiAnMDUgLSBNYXRhbGUnfSwgeydhcmVhSWQnOiA4NzA2LCAnYXJlYU5hbWUnOiAnMDYgLSBOdXdhcmEgRWxpeWEnfSwgeydhcmVhSWQnOiA5NzI1LCAnYXJlYU5hbWUnOiAnMDcgLSBHYWxsZSd9LCB7J2FyZWFJZCc6IDExMjM3LCAnYXJlYU5hbWUnOiAnMDggLSBNYXRhcmEnfSwgeydhcmVhSWQnOiAxMjE5OSwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9LCB7J2FyZWFJZCc6IDEzMDYxLCAnYXJlYU5hbWUnOiAnMTAgLSBKYWZmbmEnfSwgeydhcmVhSWQnOiAxNDM3NywgJ2FyZWFOYW1lJzogJzExIC0gVmFubmknfSwgeydhcmVhSWQnOiAxNTExNywgJ2FyZWFOYW1lJzogJzEyIC0gQmF0dGljYWxvYSd9LCB7J2FyZWFJZCc6IDE2MDA1LCAnYXJlYU5hbWUnOiAnMTMgLSBEaWdhbWFkdWxsYSd9LCB7J2FyZWFJZCc6IDE3MDk1LCAnYXJlYU5hbWUnOiAnMTQgLSBUcmluY29tYWxlZSd9LCB7J2FyZWFJZCc6IDE3NzM1LCAnYXJlYU5hbWUnOiAnMTUgLSBLdXJ1bmVnYWxhJ30sIHsnYXJlYUlkJzogMTk3NjEsICdhcmVhTmFtZSc6ICcxNiAtIFB1dHRhbGFtJ30sIHsnYXJlYUlkJzogMjA2MTEsICdhcmVhTmFtZSc6ICcxNyAtIEFudXJhZGhhcHVyYSd9LCB7J2FyZWFJZCc6IDIxOTM0LCAnYXJlYU5hbWUnOiAnMTggLSBQb2xvbm5hcnV3YSd9LCB7J2FyZWFJZCc6IDIyNTQwLCAnYXJlYU5hbWUnOiAnMTkgLSBCYWR1bGxhJ30sIHsnYXJlYUlkJzogMjM2NDQsICdhcmVhTmFtZSc6ICcyMCAtIE1vbmFyYWdhbGEnfSwgeydhcmVhSWQnOiAyNDM4MywgJ2FyZWFOYW1lJzogJzIxIC0gUmF0bmFwdXJhJ30sIHsnYXJlYUlkJzogMjU3MDEsICdhcmVhTmFtZSc6ICcyMiAtIEtlZ2FsbGUnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX25hdF9kaXNfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAxLCAnYXJlYU5hbWUnOiAnU3JpIExhbmthJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9uYXRfZGlzX3JlcF92ZXJmIjoiW3snYXJlYUlkJzogMSwgJ2FyZWFOYW1lJzogJ1NyaSBMYW5rYSd9XSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fZWNfbGVhZGVyc2hpcCI6Ilt7J2FyZWFJZCc6IDEsICdhcmVhTmFtZSc6ICdTcmkgTGFua2EnfV0ifQ.g8veK9SNHHg05Klag7JCOyYtlvJhaIqYUxWFejoyDAA",
            // window.prompt("Token"),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'X-Requested-With': 'XMLHttpRequest'
    }
});

export function request(config) {
    return axiosInstance.request(config).then((res) => res.data)
}

export function getElections() {
    return request({
        url: ENDPOINT_PATH_ELECTIONS(),
        method: 'get', // default,
    })
}

export function getElectionById(electionId) {
    return electionEntity.getById(electionId)
}

export const TALLY_SHEET_STATUS_ENUM = {
    NOT_ENTERED: "Not Entered",
    SUBMITTED: "Submitted",
    VIEWED: "Viewed",
    ENTERED: "Entered, Not Submitted",
    VERIFIED: "Verified",
    CERTIFIED: "Certified",
    NOTIFIED: "Notified",
    RELEASED: "Released"
};


async function refactorTallySheetObject(tallySheet) {
    tallySheet.tallySheetCode = tallySheet.tallySheetCode.replace(/_/g, "-");
    const {tallySheetCode, lockedVersionId, submittedVersionId, latestVersionId} = tallySheet;
    let tallySheetStatus = "";
    let readyToLock = false;
    if (COUNTING_CENTRE_WISE_DATA_ENTRY_TALLY_SHEET_CODES.indexOf(tallySheetCode) >= 0) {
        if (lockedVersionId) {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.VERIFIED;
        } else if (submittedVersionId) {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.SUBMITTED;
            readyToLock = true;
        } else if (latestVersionId) {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.ENTERED;
        } else {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.NOT_ENTERED;
        }
    } else {
        if (lockedVersionId) {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.VERIFIED;
        } else {
            tallySheetStatus = TALLY_SHEET_STATUS_ENUM.VIEWED;
            readyToLock = true
        }
    }

    tallySheet.tallySheetStatus = tallySheetStatus;
    tallySheet.readyToLock = readyToLock;
    tallySheet.area = await areaEntity.getById(tallySheet.areaId);
    tallySheet.election = await electionEntity.getById(tallySheet.electionId);
    if (COUNTING_CENTRE_WISE_DATA_ENTRY_TALLY_SHEET_CODES.indexOf(tallySheetCode) >= 0) {
        if (tallySheet.election.voteType === VOTE_TYPE.POSTAL) {
            const countingCentre = tallySheet.area;
            const electoralDistrict = getFirstOrNull(countingCentre.electoralDistricts);
            tallySheet.countingCentre = countingCentre;
            tallySheet.electoralDistrict = electoralDistrict;
        } else {
            const countingCentre = tallySheet.area;
            const pollingStation = getFirstOrNull(countingCentre.pollingStations);
            const pollingDistrict = getFirstOrNull(pollingStation.pollingDistricts);
            const pollingDivision = getFirstOrNull(pollingDistrict.pollingDivisions);
            const electoralDistrict = getFirstOrNull(pollingDivision.electoralDistricts);
            tallySheet.countingCentre = countingCentre;
            tallySheet.pollingDivision = pollingDivision;
            tallySheet.electoralDistrict = electoralDistrict;
        }
    } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_PD || tallySheetCode === TALLY_SHEET_CODE_PRE_34_I_RO || tallySheetCode === TALLY_SHEET_CODE_PRE_34_PD) {
        if (tallySheet.election.voteType === VOTE_TYPE.POSTAL) {
            tallySheet.electoralDistrict = tallySheet.area;
        } else {
            const pollingDivision = tallySheet.area;
            const electoralDistrict = getFirstOrNull(pollingDivision.electoralDistricts);
            tallySheet.pollingDivision = pollingDivision;
            tallySheet.electoralDistrict = electoralDistrict;
        }
    } else if (tallySheetCode === TALLY_SHEET_CODE_PRE_30_ED || tallySheetCode === TALLY_SHEET_CODE_PRE_34_II_RO || tallySheetCode === TALLY_SHEET_CODE_PRE_34 || tallySheetCode === TALLY_SHEET_CODE_PRE_34_ED) {
        tallySheet.electoralDistrict = tallySheet.area;
    } else if (ALL_ISLAND_TALLY_SHEET_CODES.indexOf(tallySheetCode) >= 0) {
        tallySheet.country = tallySheet.area;
    }

    return tallySheet
}

export async function getTallySheet({electionId, areaId, tallySheetCode, limit = 20, offset = 0}) {
    const tallySheets = await request({
        url: ENDPOINT_PATH_TALLY_SHEETS(),
        method: 'get',
        params: {electionId, areaId, tallySheetCode, limit, offset}
    });

    for (let i = 0; i < tallySheets.length; i++) {
        const tallySheet = tallySheets[i];
        await refactorTallySheetObject(tallySheet);
    }

    return tallySheets;
}

export function getTallySheetById(tallySheetId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEETS_BY_ID(tallySheetId),
        method: 'get',
        params: {}
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}

export function getTallySheetVersionById(tallySheetId, tallySheetCode, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode, tallySheetVersionId),
        method: 'get',
        params: {}
    })
}


export function saveTallySheetVersion(tallySheetId, tallySheetCode, body) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID(tallySheetId, tallySheetCode),
        method: 'post',
        data: body
    })
}

export function lockTallySheet(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_LOCK(tallySheetId),
        method: 'put',
        data: {
            lockedVersionId: tallySheetVersionId
        }
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}


export function uploadTallySheetProof(formData, onUploadProgress) {
    return request({
        url: `/proof/upload`,
        method: 'put',
        data: formData,
        onUploadProgress
    });
}

export function unlockTallySheet(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_UNLOCK(tallySheetId),
        method: 'put',
        data: {
            lockedVersionId: tallySheetVersionId
        }
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}

export function submitTallySheet(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_SUBMIT(tallySheetId),
        method: 'put',
        data: {
            submittedVersionId: tallySheetVersionId
        }
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}

export function notifyTallySheet(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_NOTIFY(tallySheetId),
        method: 'put'
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}

export function releaseTallySheet(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_RELEASE(tallySheetId),
        method: 'put'
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}


export function requestEditForTallySheet(tallySheetId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_REQUEST_EDIT(tallySheetId),
        method: 'put'
    }).then((tallySheet) => {
        return refactorTallySheetObject(tallySheet);
    })
}


export function getTallySheetVersionHtml(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML(tallySheetId, tallySheetVersionId),
        method: 'get'
    })
}

export function getTallySheetVersionLetterHtml(tallySheetId, tallySheetVersionId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML(tallySheetId, tallySheetVersionId),
        method: 'get'
    })
}


export function getTallySheetProof(proofId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_PROOF(proofId),
        method: 'get'
    });
}

export function finalizeProof(proofId) {
    return request({
        url: ENDPOINT_PATH_TALLY_SHEET_PROOF_FINISH(proofId),
        method: 'put'
    });
}

export function getProofImage(fileId) {
    return request({
        url: ENDPOINT_PATH_FILE(fileId),
        method: 'get',
        responseType: 'arraybuffer'
    });
}

export function generateReport(tallySheetId, tallySheetVersionId) {
    return saveTallySheetVersion(tallySheetId, tallySheetVersionId)
}


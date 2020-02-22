import axios from 'axios';
import {TABULATION_API_URL} from "../../config";
import {getAccessToken} from "../../auth";
import {AreaEntity} from "./entities/area.entity";
import {ElectionEntity} from "./entities/election.entity";
import ExtendedElection from "../../components/election/extended-election";

export const ENDPOINT_PATH_ELECTIONS = () => "/election";
export const ENDPOINT_PATH_ELECTIONS_BY_ID = (electionId) => `/election/${electionId}`;
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
        // 'X-Jwt-Assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3VzZXJuYW1lIjoiamFuYWtAY2FyYm9uLnN1cGVyIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9hZG1pbiI6IltdIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9kYXRhX2VkaXRvciI6Ilt7J2FyZWFJZCc6IDg2NSwgJ2FyZWFOYW1lJzogJzMxJ30sIHsnYXJlYUlkJzogODY2LCAnYXJlYU5hbWUnOiAnMzInfSwgeydhcmVhSWQnOiA4NjcsICdhcmVhTmFtZSc6ICczMyd9LCB7J2FyZWFJZCc6IDg2OCwgJ2FyZWFOYW1lJzogJzM0J30sIHsnYXJlYUlkJzogODY5LCAnYXJlYU5hbWUnOiAnMzUnfSwgeydhcmVhSWQnOiA4NzAsICdhcmVhTmFtZSc6ICczNid9LCB7J2FyZWFJZCc6IDg3MSwgJ2FyZWFOYW1lJzogJzM3J30sIHsnYXJlYUlkJzogODcyLCAnYXJlYU5hbWUnOiAnMzgnfSwgeydhcmVhSWQnOiA4NzMsICdhcmVhTmFtZSc6ICczOSd9LCB7J2FyZWFJZCc6IDg3NCwgJ2FyZWFOYW1lJzogJzQwJ30sIHsnYXJlYUlkJzogODc1LCAnYXJlYU5hbWUnOiAnNDEnfSwgeydhcmVhSWQnOiA4NzYsICdhcmVhTmFtZSc6ICc0Mid9LCB7J2FyZWFJZCc6IDcsICdhcmVhTmFtZSc6ICcxJ30sIHsnYXJlYUlkJzogMTAsICdhcmVhTmFtZSc6ICcyJ30sIHsnYXJlYUlkJzogMTMsICdhcmVhTmFtZSc6ICczJ30sIHsnYXJlYUlkJzogMTYsICdhcmVhTmFtZSc6ICc0J30sIHsnYXJlYUlkJzogMTksICdhcmVhTmFtZSc6ICc1J30sIHsnYXJlYUlkJzogMjIsICdhcmVhTmFtZSc6ICc2J30sIHsnYXJlYUlkJzogMjUsICdhcmVhTmFtZSc6ICc3J30sIHsnYXJlYUlkJzogMTg3LCAnYXJlYU5hbWUnOiAnOCd9LCB7J2FyZWFJZCc6IDE5MCwgJ2FyZWFOYW1lJzogJzExJ30sIHsnYXJlYUlkJzogMTkzLCAnYXJlYU5hbWUnOiAnMTAnfSwgeydhcmVhSWQnOiAxOTgsICdhcmVhTmFtZSc6ICcxMid9LCB7J2FyZWFJZCc6IDIwMywgJ2FyZWFOYW1lJzogJzknfSwgeydhcmVhSWQnOiAzNDUsICdhcmVhTmFtZSc6ICcxMyd9LCB7J2FyZWFJZCc6IDM0OCwgJ2FyZWFOYW1lJzogJzE0J30sIHsnYXJlYUlkJzogMzUxLCAnYXJlYU5hbWUnOiAnMTUnfSwgeydhcmVhSWQnOiAzNTQsICdhcmVhTmFtZSc6ICcxNid9LCB7J2FyZWFJZCc6IDM1NywgJ2FyZWFOYW1lJzogJzE3J30sIHsnYXJlYUlkJzogMzYwLCAnYXJlYU5hbWUnOiAnMTgnfSwgeydhcmVhSWQnOiAzNjMsICdhcmVhTmFtZSc6ICcxOSd9LCB7J2FyZWFJZCc6IDM2NiwgJ2FyZWFOYW1lJzogJzIwJ30sIHsnYXJlYUlkJzogNTYyLCAnYXJlYU5hbWUnOiAnMjEnfSwgeydhcmVhSWQnOiA1NjUsICdhcmVhTmFtZSc6ICcyMid9LCB7J2FyZWFJZCc6IDU2OCwgJ2FyZWFOYW1lJzogJzIzJ30sIHsnYXJlYUlkJzogNTcxLCAnYXJlYU5hbWUnOiAnMjQnfSwgeydhcmVhSWQnOiA1NzQsICdhcmVhTmFtZSc6ICcyNSd9LCB7J2FyZWFJZCc6IDU3NywgJ2FyZWFOYW1lJzogJzI2J30sIHsnYXJlYUlkJzogNTgwLCAnYXJlYU5hbWUnOiAnMjcnfSwgeydhcmVhSWQnOiA1ODMsICdhcmVhTmFtZSc6ICcyOCd9LCB7J2FyZWFJZCc6IDU4NiwgJ2FyZWFOYW1lJzogJzI5J30sIHsnYXJlYUlkJzogNTg5LCAnYXJlYU5hbWUnOiAnMzAnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAzLCAnYXJlYU5hbWUnOiAnQS1NdWxraXJpZ2FsYSd9LCB7J2FyZWFJZCc6IDE4NSwgJ2FyZWFOYW1lJzogJ0ItQmVsaWF0dGEnfSwgeydhcmVhSWQnOiAzNDMsICdhcmVhTmFtZSc6ICdDIC1UYW5nYWxsZSd9LCB7J2FyZWFJZCc6IDU2MCwgJ2FyZWFOYW1lJzogJ0QtIFRpc3NhbWFoYXJhbWEnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZlcmYiOiJbeydhcmVhSWQnOiAzLCAnYXJlYU5hbWUnOiAnQS1NdWxraXJpZ2FsYSd9LCB7J2FyZWFJZCc6IDE4NSwgJ2FyZWFOYW1lJzogJ0ItQmVsaWF0dGEnfSwgeydhcmVhSWQnOiAzNDMsICdhcmVhTmFtZSc6ICdDIC1UYW5nYWxsZSd9LCB7J2FyZWFJZCc6IDU2MCwgJ2FyZWFOYW1lJzogJ0QtIFRpc3NhbWFoYXJhbWEnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDkgLSBIYW1iYW50b3RhJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9lbGNfZGlzX3JlcF92ZXJmIjoiW3snYXJlYUlkJzogMiwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9XSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fbmF0X2Rpc19yZXBfdmlldyI6IltdIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9uYXRfZGlzX3JlcF92ZXJmIjoiW10iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VjX2xlYWRlcnNoaXAiOiJbXSJ9.uScN6UOLRd7Ep95k8PpLiSUzQbnOgR0PjuFR76a77so',
        'X-Jwt-Assertion': window.prompt("'X-Jwt-Assertion': "),
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

export function getAreas({electionId, associatedAreaId, areaType, limit = 10000, offset = 0}) {
    return request({
        url: ENDPOINT_PATH_AREAS(),
        method: 'get', // default,
        params: {electionId, associatedAreaId, areaType, limit, offset}
    })
}

export function getAreaById(areaId) {
    return request({
        url: ENDPOINT_PATH_AREAS_BY_ID(areaId),
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
    const {lockedVersionId, submittedVersionId, latestVersionId} = tallySheet;
    let tallySheetStatus = "";
    let readyToLock = false;
    if (!tallySheet.template.isDerived) {
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

    tallySheet.metaDataMap = {};
    for (let i = 0; i < tallySheet.metaDataList.length; i++) {
        const {metaDataKey, metaDataValue} = tallySheet.metaDataList[i];
        tallySheet.metaDataMap[metaDataKey] = metaDataValue;
    }

    const extendedElection = ExtendedElection(tallySheet.election);
    tallySheet = await extendedElection.mapRequiredAreasToTallySheet(tallySheet);

    return tallySheet
}

export async function getTallySheet({electionId, areaId, tallySheetCode, limit = 10000, offset = 0}) {
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


export function saveTallySheetVersion(tallySheetId, tallySheetCode, body = {}) {
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

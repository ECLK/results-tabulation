export function getMetaDataMap(metaDataList) {
    const metaDataMap = {};
    for (let i = 0; i < metaDataList.length; i++) {
        const {metaDataKey, metaDataValue} = metaDataList[i];
        metaDataMap[metaDataKey] = metaDataValue;
    }

    return metaDataMap;
}

export function getPartyMap(partyList) {
    const partyMap = {};
    for (let i = 0; i < partyList.length; i++) {
        const party = partyList[i];
        const {partyId, candidates} = party;
        party.candidateMap = getCandidateMap(candidates);

        partyMap[partyId] = party;
    }

    return partyMap;
}

export function getCandidateMap(candidateList) {
    const candidateMap = {};
    for (let i = 0; i < candidateList.length; i++) {
        const candidate = candidateList[i];
        const {candidateId} = candidate;
        candidateMap[candidateId] = candidate;
    }

    return candidateMap;
}

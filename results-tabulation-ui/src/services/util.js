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
        const {partyId} = party;
        partyMap[partyId] = party;
    }

    return partyMap;
}
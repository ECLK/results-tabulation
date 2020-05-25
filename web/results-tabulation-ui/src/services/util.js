export function getMetaDataMap(metaDataList) {
    const metaDataMap = {};
    for (let i = 0; i < metaDataList.length; i++) {
        const {metaDataKey, metaDataValue} = metaDataList[i];
        metaDataMap[metaDataKey] = metaDataValue;
    }

    return metaDataMap;
}
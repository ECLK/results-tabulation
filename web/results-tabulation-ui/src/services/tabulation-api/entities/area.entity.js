import Entity from "./entity";


const AREA_TYPE_LIST_NAMES_ENUM = {
    "PollingStation": "pollingStations",
    "PollingDistrict": "pollingDistricts",
    "CountingCentre": "countingCentres",
    "PollingDivision": "pollingDivisions",
    "ElectoralDistrict": "electoralDistricts",
    "Country": "countries",
    "DistrictCentre": "districtCentres"
};

function getChildAreaListName({areaType}) {
    return AREA_TYPE_LIST_NAMES_ENUM[areaType];
}

function appendChildArea(parentArea, childArea) {
    const childAreaListName = getChildAreaListName(childArea);
    let childAreaList = parentArea[childAreaListName];
    if (!childAreaList) {
        childAreaList = [];
        parentArea[childAreaListName] = childAreaList;
    }

    childAreaList.push(childArea)
}


export class AreaEntity extends Entity {
    AREA_TYPE_LIST_NAMES_ENUM = {
        "PollingStation": "pollingStations",
        "PollingDistrict": "pollingDistricts",
        "CountingCentre": "countingCentres",
        "PollingDivision": "pollingDivisions",
        "ElectoralDistrict": "electoralDistricts",
        "Country": "countries",
        "DistrictCentre": "districtCentres"
    }

    constructor() {
        super("area");
    }


    async pushList(list, pk) {
        await super.pushList(list, pk);

        //Map the children
        for (let i = 0; i < list.length; i++) {
            const parentArea = list[i];
            const {children} = parentArea;
            for (let j = 0; j < children.length; j++) {
                const childAreaId = children[j];
                const childArea = await this.getById(childAreaId);
                appendChildArea(parentArea, childArea);
                appendChildArea(childArea, parentArea);
            }
            this.push(list[i], pk);
        }
    }
}

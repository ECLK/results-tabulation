import Entity from "./entity";
import * as tabulationApi from "../index";


const AREA_TYPE_LIST_NAMES_ENUM = {
    "PollingStation": "pollingStationIds",
    "PollingDistrict": "pollingDistrictIds",
    "CountingCentre": "countingCentreIds",
    "PollingDivision": "pollingDivisionIds",
    "ElectoralDistrict": "electoralDistrictIds",
    "Country": "countryIds",
    "DistrictCentre": "districtCentreIds",
    "ElectionCommission": "electionCommissionIds"
};

function getChildAreaListName({areaType}) {
    return AREA_TYPE_LIST_NAMES_ENUM[areaType];
}

function appendChildArea(parentArea, childArea) {
    if (parentArea && childArea) {
        const childAreaListName = getChildAreaListName(childArea);
        let childAreaList = parentArea[childAreaListName];
        if (!childAreaList) {
            childAreaList = [];
            parentArea[childAreaListName] = childAreaList;
        }

        childAreaList.push(childArea.areaId)
    } else {
        console.log("==== appendChildArea [incomplete] ", [parentArea, childArea])
    }
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
    };

    constructor() {
        super("area");
    }

    async buildAreaParentsAndChildren() {
        const areaIdList = this.list();
        const areaMap = this.map();

        for (let j = 0; j < areaIdList.length; j++) {
            const areaId = areaIdList[j];
            const area = areaMap[areaId];

            if (area.built) {
                continue;
            } else {
                area.built = true;
            }

            for (let i = 0; i < area.parents.length; i++) {
                const parentArea = await this.getById(area.parents[i]);
                appendChildArea(area, parentArea);
                appendChildArea(parentArea, area);
            }

            for (let i = 0; i < area.children.length; i++) {
                const childArea = await this.getById(area.children[i]);
                appendChildArea(area, childArea);
                appendChildArea(childArea, area);
            }
        }
    }

    async fetchAndPush(areaId) {
        let area = await super.getById(areaId);

        if (!area) {
            area = {
                areaId,
                request: new Promise(async (resolve, reject) => {
                    try {
                        area = await tabulationApi.getAreaById(areaId);

                        delete area.request;
                        area = await this.push(area, "areaId");

                        resolve(area);
                    } catch (error) {
                        reject(error)
                    }
                })
            };
            area = await this.push(area, "areaId");
            area = await area.request;

            area = await this.push(area, "areaId");

        } else if (area) {
            if (area.request) {
                area = await area.request;
            }
        }

        return area;
    }

    async getAreas(electionId = null, associatedAreaId = null, areaType = null) {
        const areas = await tabulationApi.getAreas({electionId, associatedAreaId, areaType});

        for (let i = 0; i < areas.length; i++) {
            const area = areas[i];
            area.built = false;
            this.push(area, "areaId");
        }

        return areas
    }
}

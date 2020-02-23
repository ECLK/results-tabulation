import Entity from "./entity";
import * as tabulationApi from "../index";


export class AreaEntity extends Entity {
    constructor() {
        super("area");
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

    async getById(areaId) {
        let area = await super.getById(areaId);
        if (!area) {
            area = await this.fetchAndPush(areaId);
        }

        return area
    }
}

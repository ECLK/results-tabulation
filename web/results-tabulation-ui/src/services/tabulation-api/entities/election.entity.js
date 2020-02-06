import {ENDPOINT_PATH_ELECTION_AREA, ENDPOINT_PATH_ELECTIONS_BY_ID, request} from "../index";
import Entity from "./entity";
import {AreaEntity} from "./area.entity";


export class ElectionEntity extends Entity {
    constructor() {
        super("election");
        this.areas = new AreaEntity()
    }

    async push(obj, pk, buildAreas = true) {

        const election = await super.push(obj, pk);
        buildAreas && await this.buildAreas(obj[pk]);

        return election;
    }

    async buildAreas(electionId) {

        const areas = await request({
            url: ENDPOINT_PATH_ELECTION_AREA(electionId),
            method: 'get', // default,
        });


        await this.areas.pushList(areas, "areaId");
    }

    async fetchAndPush(electionId) {
        const election = await request({
            url: ENDPOINT_PATH_ELECTIONS_BY_ID(electionId),
            method: 'get', // default,
        });

        return await this.push(election, "electionId");
    }

    async getById(electionId) {
        let election = await super.getById(electionId);
        if (!election) {
            election = await this.fetchAndPush(electionId);
            for (let i = 0; i < election.subElections.length; i++) {
                const subElection = election.subElections[i];
                await this.push(subElection, "electionId", false);
            }
        }

        return election;
    }
}
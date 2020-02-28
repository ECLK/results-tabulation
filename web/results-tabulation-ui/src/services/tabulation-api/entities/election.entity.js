import {ENDPOINT_PATH_ELECTIONS_BY_ID, request} from "../index";
import Entity from "./entity";
import * as tabulationApi from "../index";

export class ElectionEntity extends Entity {
    constructor() {
        super("election");
    }

    async push(obj, pk) {
        const election = await super.push(obj, pk);
        this.buildPartiesAndCandidates(election);

        return election;
    }

    buildPartiesAndCandidates(election) {
        const {parties} = election;
        const partyMap = {};
        for (let i = 0; i < parties.length; i++) {
            const party = parties[i];
            const {candidates} = party;
            const candidateMap = {};

            for (let j = 0; j < candidates.length; j++) {
                const candidate = candidates[j];
                candidateMap[candidate.candidateId] = candidate;
            }

            party.candidateMap = candidateMap;
            partyMap[party.partyId] = party;
        }

        election.partyMap = partyMap;

        return election;
    }

    async fetchAndPush(electionId) {
        let election = await request({
            url: ENDPOINT_PATH_ELECTIONS_BY_ID(electionId),
            method: 'get', // default,
        });

        return await this.push(election, "electionId");
    }

    async getById(electionId, fetchSubElections = true) {
        let election = await super.getById(electionId);
        if (!election) {
            election = await this.fetchAndPush(electionId);
        }


        if (fetchSubElections) {
            for (let i = 0; i < election.subElections.length; i++) {
                const subElection = election.subElections[i];
                const subElectionId = subElection.electionId;
                Object.assign(subElection, await this.getById(subElectionId));
            }
        }

        const {parentElection} = election;
        if (parentElection) {
            const parentElectionId = parentElection.electionId;
            Object.assign(parentElection, await this.getById(parentElectionId, false))
        }

        return election;
    }
}

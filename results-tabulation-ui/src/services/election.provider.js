import React, {useState} from "react";
import {
    ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID,
    ENDPOINT_PATH_ELECTIONS,
    ENDPOINT_PATH_ELECTIONS_BY_ID,
    request
} from "./tabulation-api";
import {getMetaDataMap, getPartyMap} from "./util";

export const ElectionContext = React.createContext([]);


export function ElectionProvider(props) {
    const [state, setState] = useState({
        electionMap: {},
        electionList: {}
    });

    const saveElectionToState = (election) => {
        const {electionId, metaDataList = [], parties} = election;
        if (!election.metaDataMap) {
            election.metaDataMap = getMetaDataMap(metaDataList);
        }

        if (!election.partyMap) {
            election.partyMap = getPartyMap(parties);
        }

        // To avoid duplicated election fetches while state update wait
        state.electionMap[electionId] = {...election};

        setState(prevState => {
            return {
                ...prevState,
                electionMap: {
                    ...prevState.electionMap,
                    ...state.electionMap,
                }
            }
        });
    };

    const getElections = async ({parentElectionId = null, rootElectionId = null}) => {
        const params = {parentElectionId, rootElectionId};
        const paramsJsonString = JSON.stringify(params);

        let elections = state.electionList[paramsJsonString];

        if (!elections) {
            elections = await request({
                url: ENDPOINT_PATH_ELECTIONS(),
                method: 'get', // default,
                params: params
            });

            // To avoid duplicated elections fetches while state update wait
            state.electionList[paramsJsonString] = elections;

            setState(prevState => {
                return {
                    ...prevState,
                    electionList: {
                        ...prevState.electionList,
                        ...state.electionList
                    }
                }
            });
        }

        return elections;
    };

    const getSubElections = async (electionId) => {
        const subElections = await getElections({parentElectionId: electionId});

        return subElections;
    };


    const getParentElection = async (electionId) => {
        const election = await getElectionById(electionId);
        if (election) {
            const {parentElectionId} = election;
            if (parentElectionId) {
                return await getElectionById(parentElectionId);
            }
        }
    };

    const getElectionById = async (electionId) => {
        let election = state.electionMap[electionId];

        if (electionId && !election) {
            election = await request({
                url: ENDPOINT_PATH_ELECTIONS_BY_ID(electionId),
                method: 'get', // default,
            });

            saveElectionToState(election);
        }

        return election;
    };


    const getElectionAreaMap = async (electionId) => {
        let election = await getElectionById(electionId);

        if (!election.electionAreaMap) {
            const electionAreaMap = await request({
                url: ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID(electionId),
                method: 'get', // default,
            });

            saveElectionToState(Object.assign(election, {electionAreaMap}));
        }

        return election.electionAreaMap;
    };

    return <ElectionContext.Provider
        value={{
            getElectionById: getElectionById,
            getElections: getElections,
            getSubElections: getSubElections,
            getParentElection: getParentElection,
            getElectionAreaMap: getElectionAreaMap
        }}
    >
        {props.children}
    </ElectionContext.Provider>
}

export const ElectionConsumer = ElectionContext.Consumer;

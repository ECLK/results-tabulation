import React, {useState} from "react";
import {
    ENDPOINT_PATH_ELECTIONS,
    ENDPOINT_PATH_ELECTIONS_BY_ID,
    request
} from "./tabulation-api";
import {getMetaDataMap} from "./util";

export const ElectionContext = React.createContext([]);


export function ElectionProvider(props) {
    const [state, setState] = useState({
        electionMap: {},
        electionList: {}
    });

    const saveElectionToState = (election) => {
        const {electionId, metaDataList = []} = election;
        election.metaDataMap = getMetaDataMap(metaDataList);

        setState(prevState => {
            return {
                ...prevState,
                electionMap: {
                    ...prevState.electionMap,
                    [electionId]: {...election}
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

            setState(prevState => {
                return {
                    ...prevState,
                    electionList: {
                        ...prevState.electionList,
                        [paramsJsonString]: elections
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

    return <ElectionContext.Provider
        value={{
            getElectionById: getElectionById,
            getElections: getElections,
            getSubElections: getSubElections,
            getParentElection: getParentElection
        }}
    >
        {props.children}
    </ElectionContext.Provider>
}

export const ElectionConsumer = ElectionContext.Consumer;

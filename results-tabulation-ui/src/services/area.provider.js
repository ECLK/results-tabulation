import React, {useState} from "react";
import {ElectionContext} from "./election.provider";
import {
    ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID,
    request
} from "./tabulation-api";


export const AreaContext = React.createContext([]);
const ENDPOINT_PATH_ELECTION_MAPPED_AREA_MAP_BY_ID = (electionId) => `/election/${electionId}/mapped-area`;


export function AreaProvider(props) {
    const [state, setState] = useState({
        areaMap: {},
    });

    const saveAreaMapToState = (areaMap, areaId) => {

        // To avoid duplicated areaMap fetches while state update wait
        state.areaMap[areaId] = {...areaMap};

        setState(prevState => {
            return {
                ...prevState,
                areaMap: {
                    ...prevState.areaMap,
                    ...state.areaMap,
                }
            }
        });
    };

    const getElectionMappedArea = async (electionId) => {
        let election = await ElectionContext.getElectionById(electionId);

        if (!election.electionAreaMap) {
            const electionAreaMap = await request({
                url: ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID(electionId),
                method: 'get', // default,
            });

            saveAreaMapToState(Object.assign(election, {electionAreaMap}));
        }

        return election.electionAreaMap;
    };

    return <AreaContext.Provider
        value={{
            getElectionMappedArea: getElectionMappedArea
        }}
    >
        {props.children}
    </AreaContext.Provider>
}

export const AreaConsumer = AreaContext.Consumer;

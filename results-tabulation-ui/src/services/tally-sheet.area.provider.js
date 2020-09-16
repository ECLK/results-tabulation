import React, {useState} from "react";
import {
    ENDPOINT_PATH_ELECTION_MAPPED_AREA_BY_ID,
    request
} from "./tabulation-api";

export const TallySheetAreaContext = React.createContext([]);

export function TallySheetAreaProvider(props) {
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

    async function fetchTallySheetMappedArea(electionId, tallySheetIds, areaType) {
        let newTallySheetIds = [];

        // fetch only new tally sheet ids
        for (const [index, value] of tallySheetIds.entries()) {
            if (!state.areaMap[value]) {
                newTallySheetIds.push(value)
            }
        }
        console.log(newTallySheetIds.toString());
        if (newTallySheetIds.length > 0) {
            const electionMappedArea = await request({
                url: ENDPOINT_PATH_ELECTION_MAPPED_AREA_BY_ID(electionId,tallySheetIds, areaType),
                method: 'get', // default,
            });

            console.log(electionMappedArea);

            // saveAreaMapToState(Object.assign(election, {electionAreaMap}));
        }

        return "hello2";
    }

    return <TallySheetAreaContext.Provider
        value={{
            fetchTallySheetMappedArea
        }}
    >
        {props.children}
    </TallySheetAreaContext.Provider>
}

export const TallySheetAreaConsumer = TallySheetAreaContext.Consumer;

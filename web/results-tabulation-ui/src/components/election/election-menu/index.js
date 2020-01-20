import React from "react";
import PRESIDENTIAL_ELECTION_2019 from "./PRESIDENTIAL_ELECTION_2019";
import PARLIAMENT_ELECTION_2020 from "./PARLIAMENT_ELECTION_2020";

const ELECTION_TEMPLATE_NAME = {
    PRESIDENTIAL_ELECTION_2019: "PRESIDENTIAL_ELECTION_2019",
    PARLIAMENT_ELECTION_2020: "PARLIAMENT_ELECTION_2020"
};

export default function ElectionMenu({election}) {
    const {electionTemplateName} = election;
    let electionMenu = null;

    switch (electionTemplateName) {
        case ELECTION_TEMPLATE_NAME.PRESIDENTIAL_ELECTION_2019:
            electionMenu = <PRESIDENTIAL_ELECTION_2019 election={election}/>;
            break;
        case ELECTION_TEMPLATE_NAME.PARLIAMENT_ELECTION_2020:
            electionMenu = <PARLIAMENT_ELECTION_2020 election={election}/>;
            break;
        default:
            electionMenu = null;
    }

    return electionMenu;
}



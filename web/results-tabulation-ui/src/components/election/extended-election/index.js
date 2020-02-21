import ExtendedElectionPresidentialElection2019 from "./PresidentialElection2019";
import ExtendedElectionParliamentElection2020 from "./ParliamentElection2020";
import ExtendedElectionDefault from "./extended-election-default";

const ELECTION_TEMPLATE_NAME = {
    PRESIDENTIAL_ELECTION_2019: "PRESIDENTIAL_ELECTION_2019",
    PARLIAMENT_ELECTION_2020: "PARLIAMENT_ELECTION_2020"
};

export default function (election) {
    return getExtendedElection(election);
}

export function getExtendedElectionClass(election) {
    const {electionTemplateName} = election.rootElection;
    let extendedElectionClass;

    switch (electionTemplateName) {
        case ELECTION_TEMPLATE_NAME.PRESIDENTIAL_ELECTION_2019:
            extendedElectionClass = ExtendedElectionPresidentialElection2019;
            break;
        case ELECTION_TEMPLATE_NAME.PARLIAMENT_ELECTION_2020:
            extendedElectionClass = ExtendedElectionParliamentElection2020;
            break;
        default:
            extendedElectionClass = ExtendedElectionDefault;
    }

    return extendedElectionClass;
}

export function getExtendedElection(election) {
    const extendedElectionClass = getExtendedElectionClass(election);

    return new extendedElectionClass(election);
}

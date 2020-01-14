def get_extended_election_class(electionTemplateName):
    from constants.ELECTION_TEMPLATES import PRESIDENTIAL_ELECTION_2019, PARLIAMENT_ELECTION_2020
    from ext.Election import PresidentialElection2019, ParliamentaryElection2020

    EXTENDED_ELECTION_MAP = {
        PRESIDENTIAL_ELECTION_2019: PresidentialElection2019,
        PARLIAMENT_ELECTION_2020: ParliamentaryElection2020
    }

    if electionTemplateName in EXTENDED_ELECTION_MAP:
        return EXTENDED_ELECTION_MAP[electionTemplateName]
    else:
        return None


def get_role_based_access_config(electionTemplateName):
    extended_election_class = get_extended_election_class(electionTemplateName=electionTemplateName)

    if extended_election_class is not None:
        return extended_election_class.role_based_access_config
    else:
        return None

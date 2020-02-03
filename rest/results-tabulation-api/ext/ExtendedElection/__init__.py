def get_extended_election(election):
    from constants.ELECTION_TEMPLATES import PRESIDENTIAL_ELECTION_2019, PARLIAMENT_ELECTION_2020
    from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import ExtendedElectionParliamentaryElection2020
    from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import ExtendedElectionPresidentialElection2019

    EXTENDED_ELECTION_MAP = {
        PRESIDENTIAL_ELECTION_2019: ExtendedElectionPresidentialElection2019,
        PARLIAMENT_ELECTION_2020: ExtendedElectionParliamentaryElection2020
    }

    if election.electionTemplateName in EXTENDED_ELECTION_MAP:
        return EXTENDED_ELECTION_MAP[election.electionTemplateName](election=election)
    else:
        return None


class ExtendedElection:
    from orm.entities import Election

    role_based_access_config = None

    def __init__(self, election, role_based_access_config=None):
        self.election = election
        self.role_based_access_config = role_based_access_config

    def get_extended_tally_sheet_version_class(self, templateName):
        from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion import ExtendedTallySheetVersion

        EXTENDED_TEMPLATE_MAP = {
            # TODO
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return ExtendedTallySheetVersion

    def build_election(root_election: Election, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None):
        pass

from constants.AUTH_CONSTANTS import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import PRE_41, PRE_30_PD, \
    PRE_30_ED, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, \
    PRE_ALL_ISLAND_RESULTS, CE_201_PV, CE_201, PRE_34_PD, PRE_34_ED, PRE_34_AI
from constants.VOTE_TYPES import Postal, NonPostal, PostalAndNonPostal
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_SAVE

READ = WORKFLOW_ACTION_TYPE_VIEW
WRITE = WORKFLOW_ACTION_TYPE_SAVE


role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PRE_41: {
            NonPostal: [READ, WRITE],
            Postal: [READ, WRITE]
        },
        CE_201: {
            NonPostal: [READ, WRITE]
        },
        CE_201_PV: {
            Postal: [READ, WRITE]
        },
        PRE_34_CO: {
            NonPostal: [READ, WRITE],
            Postal: [READ, WRITE]
        },

    },
    POLLING_DIVISION_REPORT_VIEWER_ROLE: {
        PRE_30_PD: {
            NonPostal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            NonPostal: [READ, WRITE]
        },
        PRE_34_PD: {
            NonPostal: [READ, WRITE]
        }
    },
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: {
        PRE_41: {
            NonPostal: [READ]
        },
        CE_201: {
            NonPostal: [READ]
        },
        PRE_34_CO: {
            NonPostal: [READ]
        },
        PRE_30_PD: {
            NonPostal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            NonPostal: [READ, WRITE]
        },
        PRE_34_PD: {
            NonPostal: [READ, WRITE]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: {
        PRE_30_PD: {
            Postal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: {
        PRE_41: {
            Postal: [READ]
        },
        CE_201_PV: {
            Postal: [READ]
        },
        PRE_34_CO: {
            Postal: [READ]
        },
        PRE_30_PD: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    NATIONAL_REPORT_VIEWER_ROLE: {
        PRE_ALL_ISLAND_RESULTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_AI: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    NATIONAL_REPORT_VERIFIER_ROLE: {
        PRE_30_PD: {
            Postal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_ALL_ISLAND_RESULTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_AI: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    EC_LEADERSHIP_ROLE: {
        PRE_41: {
            Postal: [READ],
            NonPostal: [READ]
        },
        CE_201: {
            NonPostal: [READ]
        },
        CE_201_PV: {
            Postal: [READ]
        },
        PRE_34_CO: {
            Postal: [READ],
            NonPostal: [READ]
        },
        PRE_30_PD: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE],
            NonPostal: [READ, WRITE]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_ALL_ISLAND_RESULTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PRE_34_AI: {
            PostalAndNonPostal: [READ, WRITE]
        }
    }
}

from constants.AUTH_CONSTANTS import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, ACCESS_TYPE_READ, ACCESS_TYPE_LOCK, \
    ACCESS_TYPE_UNLOCK, \
    ACCESS_TYPE_WRITE, ACCESS_TYPE_SUBMIT
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import PRE_41, PRE_30_PD, \
    PRE_30_ED, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, \
    PRE_ALL_ISLAND_RESULTS, CE_201_PV, CE_201, PRE_34_PD, PRE_34_ED, PRE_34_AI
from constants.VOTE_TYPES import Postal, NonPostal, PostalAndNonPostal

READ = ACCESS_TYPE_READ
WRITE = ACCESS_TYPE_WRITE
SUBMIT = ACCESS_TYPE_SUBMIT
LOCK = ACCESS_TYPE_LOCK
UNLOCK = ACCESS_TYPE_UNLOCK

role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PRE_41: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        CE_201: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK]
        },
        CE_201_PV: {
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        PRE_34_CO: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
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
            NonPostal: [READ, UNLOCK]
        },
        CE_201: {
            NonPostal: [READ, UNLOCK]
        },
        PRE_34_CO: {
            NonPostal: [READ, UNLOCK]
        },
        PRE_30_PD: {
            NonPostal: [READ, WRITE, LOCK]
        },
        PRE_34_I_RO: {
            NonPostal: [READ, WRITE, LOCK]
        },
        PRE_34_PD: {
            NonPostal: [READ, WRITE, LOCK]
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
            Postal: [READ, UNLOCK]
        },
        CE_201_PV: {
            Postal: [READ, UNLOCK]
        },
        PRE_34_CO: {
            Postal: [READ, UNLOCK]
        },
        PRE_30_PD: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
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
    NATIONAL_REPORT_VIEWER_ROLE: {
        PRE_30_PD: {
            Postal: [READ, WRITE, UNLOCK]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE, UNLOCK]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE, UNLOCK]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_ALL_ISLAND_RESULTS: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PRE_34_AI: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
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
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_I_RO: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_PD: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_30_ED: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_II_RO: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_ED: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_ALL_ISLAND_RESULTS: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PRE_34_AI: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        }
    }
}

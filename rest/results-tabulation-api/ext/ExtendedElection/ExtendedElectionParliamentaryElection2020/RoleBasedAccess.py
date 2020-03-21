from constants.AUTH_CONSTANTS import ACCESS_TYPE_READ, ACCESS_TYPE_LOCK, ACCESS_TYPE_UNLOCK, ACCESS_TYPE_WRITE, \
    ACCESS_TYPE_SUBMIT, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, \
    NATIONAL_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from constants.VOTE_TYPES import NonPostal, Postal, PostalAndNonPostal
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import PE_27, CE_201, CE_201_PV, PE_4, PE_CE_RO_V1, \
    PE_R1, PE_CE_RO_PR_1, PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, PE_39, PE_22, PE_21, POLLING_DIVISION_RESULTS, ALL_ISLAND_RESULT

READ = ACCESS_TYPE_READ
WRITE = ACCESS_TYPE_WRITE
SUBMIT = ACCESS_TYPE_SUBMIT
LOCK = ACCESS_TYPE_LOCK
UNLOCK = ACCESS_TYPE_UNLOCK

role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PE_27: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        PE_39: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        PE_22: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        CE_201: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK]
        },
        CE_201_PV: {
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
        PE_4: {
            NonPostal: [READ, WRITE, SUBMIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, LOCK]
        },
    },
    POLLING_DIVISION_REPORT_VIEWER_ROLE: {
        PE_CE_RO_V1: {
            NonPostal: [READ, WRITE]
        },
        POLLING_DIVISION_RESULTS: {
            NonPostal: [READ, WRITE]
        },
        PE_R1: {
            NonPostal: [READ, WRITE]
        },
        PE_CE_RO_PR_1: {
            NonPostal: [READ, WRITE]
        }
    },
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: {
        PE_27: {
            NonPostal: [READ, UNLOCK]
        },
        PE_39: {
            NonPostal: [READ, UNLOCK]
        },
        PE_22: {
            NonPostal: [READ, UNLOCK]
        },
        CE_201: {
            NonPostal: [READ, UNLOCK]
        },
        PE_4: {
            NonPostal: [READ, UNLOCK]
        },
        PE_CE_RO_V1: {
            NonPostal: [READ, WRITE, LOCK]
        },
        POLLING_DIVISION_RESULTS: {
            NonPostal: [READ, WRITE, LOCK]
        },
        PE_R1: {
            NonPostal: [READ, WRITE, LOCK]
        },
        PE_CE_RO_PR_1: {
            NonPostal: [READ, WRITE, LOCK]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: {
        PE_CE_RO_V1: {
            Postal: [READ, WRITE]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, WRITE]
        },
        PE_R1: {
            Postal: [READ, WRITE]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, WRITE]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, WRITE]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: {
        PE_27: {
            Postal: [READ, UNLOCK]
        },
        PE_39: {
            Postal: [READ, UNLOCK]
        },
        PE_22: {
            Postal: [READ, UNLOCK]
        },
        CE_201_PV: {
            Postal: [READ, UNLOCK]
        },
        PE_4: {
            Postal: [READ, UNLOCK]
        },
        PE_CE_RO_V1: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_R1: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, WRITE, LOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE, LOCK]
        }
    },
    NATIONAL_REPORT_VIEWER_ROLE: {
        ALL_ISLAND_RESULT: {
            PostalAndNonPostal: [READ, WRITE]
        }
    },
    NATIONAL_REPORT_VERIFIER_ROLE: {
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        ALL_ISLAND_RESULT: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        }
    },
    EC_LEADERSHIP_ROLE: {
        PE_27: {
            Postal: [READ, UNLOCK],
            NonPostal: [READ, UNLOCK]
        },
        PE_39: {
            Postal: [READ, UNLOCK],
            NonPostal: [READ, UNLOCK]
        },
        PE_22: {
            Postal: [READ, UNLOCK],
            NonPostal: [READ, UNLOCK]
        },
        CE_201_PV: {
            Postal: [READ, UNLOCK]
        },
        CE_201: {
            NonPostal: [READ, UNLOCK]
        },
        PE_4: {
            Postal: [READ, UNLOCK],
            NonPostal: [READ, UNLOCK]
        },
        PE_CE_RO_V1: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_R1: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        ALL_ISLAND_RESULT: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        }
    }
}

from constants.AUTH_CONSTANTS import DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from constants.VOTE_TYPES import NonPostal, Postal, PostalAndNonPostal
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TALLY_SHEET_CODES import PE_27, CE_201, CE_201_PV, \
    PE_4, PE_CE_RO_V1, \
    PE_R1, PE_CE_RO_PR_1, PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, PE_39, PE_22, PE_21, POLLING_DIVISION_RESULTS
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, \
    WORKFLOW_ACTION_TYPE_RELEASE, WORKFLOW_ACTION_TYPE_EDIT

READ = WORKFLOW_ACTION_TYPE_VIEW
WRITE = WORKFLOW_ACTION_TYPE_SAVE
SUBMIT = WORKFLOW_ACTION_TYPE_SUBMIT
EDIT = WORKFLOW_ACTION_TYPE_EDIT
LOCK = WORKFLOW_ACTION_TYPE_VERIFY
UNLOCK = WORKFLOW_ACTION_TYPE_REQUEST_CHANGES
MOVE_TO_CERTIFY = WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY
CERTIFY = WORKFLOW_ACTION_TYPE_CERTIFY
RELEASE = WORKFLOW_ACTION_TYPE_RELEASE

role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PE_27: {
            NonPostal: [READ, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_39: {
            NonPostal: [READ, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_22: {
            NonPostal: [READ, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, EDIT, LOCK]
        },
        CE_201: {
            NonPostal: [READ, WRITE, SUBMIT, EDIT, LOCK]
        },
        CE_201_PV: {
            Postal: [READ, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_4: {
            NonPostal: [READ, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, WRITE, SUBMIT, EDIT, LOCK]
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
            Postal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            NonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            NonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        PE_R1: {
            Postal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            NonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, WRITE, UNLOCK],
            NonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        }
    }
}

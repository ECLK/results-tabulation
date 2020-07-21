from constants.AUTH_CONSTANTS import DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from constants.VOTE_TYPES import NonPostal, Postal, PostalAndNonPostal, Displaced, Quarantine
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import PE_AI_ED, PE_AI_NL_1, PE_AI_NL_2, PE_AI_1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TALLY_SHEET_CODES import PE_27, CE_201, CE_201_PV, \
    PE_4, PE_CE_RO_V1, \
    PE_CE_RO_PR_1, PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, PE_39, PE_22, PE_21, POLLING_DIVISION_RESULTS, \
    PE_AI_2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, \
    WORKFLOW_ACTION_TYPE_RELEASE, WORKFLOW_ACTION_TYPE_EDIT, WORKFLOW_ACTION_TYPE_PRINT, \
    WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_PRINT_LETTER

READ = WORKFLOW_ACTION_TYPE_VIEW
PRINT = WORKFLOW_ACTION_TYPE_PRINT
PRINT_LETTER = WORKFLOW_ACTION_TYPE_PRINT_LETTER
WRITE = WORKFLOW_ACTION_TYPE_SAVE
SUBMIT = WORKFLOW_ACTION_TYPE_SUBMIT
EDIT = WORKFLOW_ACTION_TYPE_EDIT
LOCK = WORKFLOW_ACTION_TYPE_VERIFY
UNLOCK = WORKFLOW_ACTION_TYPE_REQUEST_CHANGES
MOVE_TO_CERTIFY = WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY
CERTIFY = WORKFLOW_ACTION_TYPE_CERTIFY
RELEASE = WORKFLOW_ACTION_TYPE_RELEASE
UPLOAD_PROOF_DOCUMENT = WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT

role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PE_27: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_39: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_22: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        CE_201: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        CE_201_PV: {
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_4: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
    },
    POLLING_DIVISION_REPORT_VIEWER_ROLE: {
        PE_CE_RO_V1: {
            NonPostal: [READ, PRINT, WRITE]
        },
        POLLING_DIVISION_RESULTS: {
            NonPostal: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_1: {
            NonPostal: [READ, PRINT, WRITE]
        }
    },
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: {
        PE_27: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PE_39: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PE_22: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        CE_201: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PE_4: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PE_CE_RO_V1: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        },
        POLLING_DIVISION_RESULTS: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_CE_RO_PR_1: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: {
        PE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_21: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        }
    },
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: {
        PE_27: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PE_39: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PE_22: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        CE_201_PV: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PE_4: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_21: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        }
    },
    NATIONAL_REPORT_VIEWER_ROLE: {
        PE_AI_ED: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PE_AI_NL_1: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PE_AI_NL_2: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PE_AI_1: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PE_AI_2: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        }
    },
    NATIONAL_REPORT_VERIFIER_ROLE: {
        PE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_21: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PE_AI_ED: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_AI_NL_1: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_AI_NL_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PE_AI_1: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PE_AI_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        }
    },
    EC_LEADERSHIP_ROLE: {
        PE_27: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PE_39: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PE_22: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        CE_201_PV: {
            Postal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        CE_201: {
            NonPostal: [READ, PRINT]
        },
        PE_4: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PE_CE_RO_V1: {
            Postal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            NonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            Displaced: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, RELEASE],
            Quarantine: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, RELEASE]
        },
        POLLING_DIVISION_RESULTS: {
            Postal: [READ, PRINT, WRITE],
            NonPostal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_R2: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY,
                                 RELEASE]
        },
        PE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE],
            NonPostal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PE_21: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY,
                                 RELEASE]
        },
        PE_AI_ED: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, RELEASE]
        },
        PE_AI_NL_1: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, RELEASE]
        },
        PE_AI_NL_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, RELEASE]
        },
        PE_AI_1: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, RELEASE]
        },
        PE_AI_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, RELEASE]
        }
    }
}

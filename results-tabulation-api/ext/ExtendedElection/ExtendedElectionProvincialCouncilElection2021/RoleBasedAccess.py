from constants.AUTH_CONSTANTS import DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE, ADMINISTRATIVE_DISTRICT_REPORT_VIEWER_ROLE, \
    ADMINISTRATIVE_DISTRICT_REPORT_VERIFIER_ROLE, PROVINCIAL_REPORT_VIEWER_ROLE, PROVINCIAL_REPORT_VERIFIER_ROLE
from constants.VOTE_TYPES import NonPostal, Postal, PostalAndNonPostal, Displaced, Quarantine
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201, CE_201_PV, \
    PCE_31, PCE_34, PCE_35, PCE_CE_CO_PR_1, PCE_CE_CO_PR_2, PCE_CE_CO_PR_3, PCE_CE_CO_PR_4, PCE_CE_RO_V1, PCE_R1, \
    PCE_R1_PV, PCE_CE_RO_V2, PCE_R2, PCE_CE_RO_PR_1, PCE_CE_RO_PR_2, PCE_CE_RO_PR_3, PCE_42, PCE_PD_V, PCE_PC_V, \
    PCE_PC_CD, PCE_PC_BS_1, PCE_PC_BS_2, PCE_PC_SA_1, PCE_PC_SA_2, PCE_POST_PC

from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, \
    WORKFLOW_ACTION_TYPE_RELEASE, WORKFLOW_ACTION_TYPE_EDIT, WORKFLOW_ACTION_TYPE_PRINT, \
    WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_PRINT_LETTER, WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY

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
NOTIFY = WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY
UPLOAD_PROOF_DOCUMENT = WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT
BACK_TO_VERIFIED = WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED

role_based_access_config = {
    DATA_EDITOR_ROLE: {
        PCE_35: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_34: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_31: {
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
        PCE_CE_CO_PR_4: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_42: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_R2: {
            NonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Postal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Displaced: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK],
            Quarantine: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
    },
    POLLING_DIVISION_REPORT_VIEWER_ROLE: {
        PCE_CE_RO_V1: {
            NonPostal: [READ, PRINT, WRITE]
        },
        PCE_PD_V: {
            NonPostal: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_1: {
            NonPostal: [READ, PRINT, WRITE]
        },
    },
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: {
        PCE_35: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PCE_34: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PCE_31: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        CE_201: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PCE_CE_CO_PR_4: {
            NonPostal: [READ, PRINT, UNLOCK]
        },
        PCE_CE_RO_V1: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_PD_V: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_CE_RO_PR_1: {
            NonPostal: [READ, PRINT, WRITE, LOCK]
        }
    },
    ADMINISTRATIVE_DISTRICT_REPORT_VIEWER_ROLE: {
        PCE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PCE_PD_V: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_42: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        }
    },
    ADMINISTRATIVE_DISTRICT_REPORT_VERIFIER_ROLE: {
        PCE_35: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PCE_34: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PCE_31: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        CE_201_PV: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PCE_CE_CO_PR_4: {
            Postal: [READ, PRINT, UNLOCK],
            Displaced: [READ, PRINT, UNLOCK],
            Quarantine: [READ, PRINT, UNLOCK]
        },
        PCE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        PCE_PD_V: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        PCE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE, LOCK],
            NonPostal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, LOCK],
            Quarantine: [READ, PRINT, WRITE, LOCK]
        },
        PCE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_42: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        }
    },
    PROVINCIAL_REPORT_VIEWER_ROLE: {
        PCE_PC_V: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PCE_PC_CD: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PCE_PC_BS_1: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PCE_PC_BS_2: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PCE_PC_SA_1: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        },
        PCE_PC_SA_2: {
            PostalAndNonPostal: [READ, WRITE, PRINT]
        }
    },
    PROVINCIAL_REPORT_VERIFIER_ROLE: {
        PCE_CE_RO_V1: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_PD_V: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE, UNLOCK],
            Displaced: [READ, PRINT, WRITE, UNLOCK],
            Quarantine: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_CE_RO_V2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_R2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_42: {
            PostalAndNonPostal: [READ, PRINT, WRITE, UNLOCK]
        },
        PCE_PC_V: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_PC_CD: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_PC_BS_1: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_PC_BS_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, SUBMIT, EDIT, LOCK]
        },
        PCE_PC_SA_1: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        },
        PCE_PC_SA_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE, LOCK]
        }
    },
    EC_LEADERSHIP_ROLE: {
        PCE_35: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PCE_34: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PCE_31: {
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
        PCE_CE_CO_PR_4: {
            Postal: [READ, PRINT],
            NonPostal: [READ, PRINT],
            Displaced: [READ, PRINT],
            Quarantine: [READ, PRINT]
        },
        PCE_CE_RO_V1: {
            Postal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, NOTIFY,
                     RELEASE, BACK_TO_VERIFIED],
            NonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, NOTIFY,
                        RELEASE, BACK_TO_VERIFIED],
            Displaced: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, NOTIFY,
                        RELEASE, BACK_TO_VERIFIED],
            Quarantine: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY, CERTIFY, NOTIFY,
                         RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PD_V: {
            Postal: [READ, PRINT, WRITE],
            NonPostal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_V2: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_R2: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_CE_RO_PR_1: {
            Postal: [READ, PRINT, WRITE],
            NonPostal: [READ, PRINT, WRITE],
            Displaced: [READ, PRINT, WRITE],
            Quarantine: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_2: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_CE_RO_PR_3: {
            PostalAndNonPostal: [READ, PRINT, WRITE]
        },
        PCE_42: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_V: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_CD: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_BS_1: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_BS_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_SA_1: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_PC_SA_2: {
            PostalAndNonPostal: [READ, WRITE, UNLOCK, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
        PCE_POST_PC: {
            PostalAndNonPostal: [READ, WRITE, PRINT, PRINT_LETTER, UPLOAD_PROOF_DOCUMENT, MOVE_TO_CERTIFY,
                                 CERTIFY, NOTIFY, RELEASE, BACK_TO_VERIFIED]
        },
    }
}

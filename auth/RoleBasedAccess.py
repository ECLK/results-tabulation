from auth import POLLING_DIVISION_REPORT_VERIFIER_ROLE, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    NATIONAL_REPORT_VERIFIER_ROLE
from orm.enums import TallySheetCodeEnum

role_to_read_allowed_tallysheet_types = {
    DATA_EDITOR_ROLE: [
        TallySheetCodeEnum.PRE_41,
        TallySheetCodeEnum.CE_201,
        TallySheetCodeEnum.CE_201_PV,
        TallySheetCodeEnum.PRE_34_CO
    ],
    POLLING_DIVISION_REPORT_VIEWER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD,
        TallySheetCodeEnum.PRE_34_I_RO
    ],
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD,
        TallySheetCodeEnum.PRE_34_I_RO,
        TallySheetCodeEnum.PRE_41,
        TallySheetCodeEnum.CE_201,
        TallySheetCodeEnum.CE_201_PV,
        TallySheetCodeEnum.PRE_34_CO
    ],
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD_PV,
        TallySheetCodeEnum.PRE_30_ED
    ],
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD_PV,
        TallySheetCodeEnum.PRE_30_ED,
        TallySheetCodeEnum.PRE_30_PD
    ],
    NATIONAL_REPORT_VIEWER_ROLE: [
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
    ],
    NATIONAL_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS,
        TallySheetCodeEnum.PRE_30_PD_PV,
        TallySheetCodeEnum.PRE_30_ED
    ]
}

role_to_lock_allowed_tallysheet_types = {
    DATA_EDITOR_ROLE: [
        TallySheetCodeEnum.PRE_41,
        TallySheetCodeEnum.CE_201,
        TallySheetCodeEnum.CE_201_PV,
        TallySheetCodeEnum.PRE_34_CO
    ],
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD
    ],
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD_PV,
        TallySheetCodeEnum.PRE_30_ED
    ],
    NATIONAL_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
    ]
}

role_to_unlock_allowed_tallysheet_types = {
    POLLING_DIVISION_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_41,
        TallySheetCodeEnum.CE_201,
        TallySheetCodeEnum.CE_201_PV,
        TallySheetCodeEnum.PRE_34_CO
    ],
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD
    ],
    NATIONAL_REPORT_VERIFIER_ROLE: [
        TallySheetCodeEnum.PRE_30_PD_PV,
        TallySheetCodeEnum.PRE_30_ED,
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
        TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
    ]
}

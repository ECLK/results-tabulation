import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_COUNTRY,
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT,
    TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS
} from "../../../tally-sheet/constants/TALLY_SHEET_COLUMN";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PRE_30_ED,
    TALLY_SHEET_CODE_PRE_30_PD,
    TALLY_SHEET_CODE_PRE_34, TALLY_SHEET_CODE_PRE_34_AI,
    TALLY_SHEET_CODE_PRE_34_CO,
    TALLY_SHEET_CODE_PRE_34_ED,
    TALLY_SHEET_CODE_PRE_34_I_RO,
    TALLY_SHEET_CODE_PRE_34_II_RO,
    TALLY_SHEET_CODE_PRE_34_PD,
    TALLY_SHEET_CODE_PRE_41,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS,
    TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
} from "./TALLY_SHEET_CODE";
import {
    VOTE_TYPE_NON_POSTAL,
    VOTE_TYPE_POSTAL
} from "../../constants/VOTE_TYPE";
import {
    TALLY_SHEET_LIST_ROW_ACTION_ENTER_OR_EDIT,
    TALLY_SHEET_LIST_ROW_ACTION_UNLOCK, TALLY_SHEET_LIST_ROW_ACTION_VERIFY, TALLY_SHEET_LIST_ROW_ACTION_VIEW
} from "../../../tally-sheet/constants/TALLY_SHEET_ACTION";

const columns_ed_pd_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_pd_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_country_status_actions = [
    TALLY_SHEET_LIST_COLUMN_COUNTRY, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];

export const TALLY_SHEET_LIST_COLUMNS = {
    [TALLY_SHEET_CODE_PRE_34_CO]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_cc_status_actions
    },
    [TALLY_SHEET_CODE_PRE_41]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_cc_status_actions
    },
    [TALLY_SHEET_CODE_CE_201]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions
    },
    [TALLY_SHEET_CODE_CE_201_PV]: {
        [VOTE_TYPE_POSTAL]: columns_ed_cc_status_actions
    },
    [TALLY_SHEET_CODE_PRE_30_PD]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34_I_RO]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34_PD]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_30_ED]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34_II_RO]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34_ED]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS]: {
        [undefined]: columns_country_status_actions
    },
    [TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS]: {
        [undefined]: columns_country_status_actions
    },
    [TALLY_SHEET_CODE_PRE_34_AI]: {
        [undefined]: columns_country_status_actions
    }
};

const actions_enter_view_verify_unlock = [TALLY_SHEET_LIST_ROW_ACTION_ENTER_OR_EDIT, TALLY_SHEET_LIST_ROW_ACTION_VIEW,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY, TALLY_SHEET_LIST_ROW_ACTION_UNLOCK];
const actions_view_verify_unlock = [TALLY_SHEET_LIST_ROW_ACTION_VIEW,
    TALLY_SHEET_LIST_ROW_ACTION_VERIFY, TALLY_SHEET_LIST_ROW_ACTION_UNLOCK];

export const TALLY_SHEET_LIST_ACTIONS = {
    [TALLY_SHEET_CODE_PRE_34_CO]: {
        [VOTE_TYPE_NON_POSTAL]: actions_enter_view_verify_unlock,
        [VOTE_TYPE_POSTAL]: actions_enter_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_41]: {
        [VOTE_TYPE_NON_POSTAL]: actions_enter_view_verify_unlock,
        [VOTE_TYPE_POSTAL]: actions_enter_view_verify_unlock
    },
    [TALLY_SHEET_CODE_CE_201]: {
        [VOTE_TYPE_NON_POSTAL]: actions_enter_view_verify_unlock
    },
    [TALLY_SHEET_CODE_CE_201_PV]: {
        [VOTE_TYPE_POSTAL]: actions_enter_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_30_PD]: {
        [VOTE_TYPE_NON_POSTAL]: actions_view_verify_unlock,
        [VOTE_TYPE_POSTAL]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34_I_RO]: {
        [VOTE_TYPE_NON_POSTAL]: actions_view_verify_unlock,
        [VOTE_TYPE_POSTAL]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34_PD]: {
        [VOTE_TYPE_NON_POSTAL]: actions_view_verify_unlock,
        [VOTE_TYPE_POSTAL]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_30_ED]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34_II_RO]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34_ED]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_ALL_ISLAND_RESULTS]: {
        [undefined]: actions_view_verify_unlock
    },
    [TALLY_SHEET_CODE_PRE_34_AI]: {
        [undefined]: actions_view_verify_unlock
    }
};

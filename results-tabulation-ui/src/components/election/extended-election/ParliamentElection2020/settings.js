import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_COUNTRY,
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS
} from "../../../tally-sheet/constants/TALLY_SHEET_COLUMN";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PE_27,
    TALLY_SHEET_CODE_PE_4,
    TALLY_SHEET_CODE_PE_CE_RO_PR_1,
    TALLY_SHEET_CODE_PE_CE_RO_PR_2,
    TALLY_SHEET_CODE_PE_CE_RO_PR_3,
    TALLY_SHEET_CODE_PE_CE_RO_V1,
    TALLY_SHEET_CODE_PE_CE_RO_V2,
    TALLY_SHEET_CODE_PE_R2,
    TALLY_SHEET_CODE_PE_39,
    TALLY_SHEET_CODE_PE_22,
    TALLY_SHEET_CODE_POLLING_DIVISION_RESULTS,
    TALLY_SHEET_CODE_ALL_ISLAND_RESULT
} from "./TALLY_SHEET_CODE";
import {
    VOTE_TYPE_NON_POSTAL,
    VOTE_TYPE_POSTAL
} from "../../constants/VOTE_TYPE";

const columns_ed_pd_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_pd_cc_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_PARTY, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_cc_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_pd_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_pd_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ed_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_ELECTORAL_DISTRICT, TALLY_SHEET_LIST_COLUMN_PARTY, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_country_status_actions = [
    TALLY_SHEET_LIST_COLUMN_COUNTRY, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];

export const TALLY_SHEET_LIST_COLUMNS = {
    [TALLY_SHEET_CODE_PE_27]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_cc_status_actions
    },
    [TALLY_SHEET_CODE_PE_4]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_party_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_cc_party_status_actions
    },
    [TALLY_SHEET_CODE_CE_201]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions
    },
    [TALLY_SHEET_CODE_CE_201_PV]: {
        [VOTE_TYPE_POSTAL]: columns_ed_cc_status_actions
    },
    [TALLY_SHEET_CODE_PE_CE_RO_V1]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_POLLING_DIVISION_RESULTS]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PE_CE_RO_PR_1]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_party_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_party_status_actions
    },
    [TALLY_SHEET_CODE_PE_CE_RO_PR_2]: {
        [undefined]: columns_ed_party_status_actions
    },
    [TALLY_SHEET_CODE_PE_CE_RO_PR_3]: {
        [undefined]: columns_ed_party_status_actions
    },
    [TALLY_SHEET_CODE_PE_CE_RO_V2]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PE_R2]: {
        [undefined]: columns_ed_status_actions
    },
    [TALLY_SHEET_CODE_PE_39]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_pd_cc_status_actions
    },
    [TALLY_SHEET_CODE_PE_22]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ed_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ed_pd_cc_status_actions
    },
    [TALLY_SHEET_CODE_ALL_ISLAND_RESULT]: {
        [undefined]: columns_country_status_actions
    }
};

import {
    TALLY_SHEET_LIST_COLUMN_ACTIONS,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE,TALLY_SHEET_LIST_COLUMN_PROVINCE,
    TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS
} from "../../../tally-sheet/constants/TALLY_SHEET_COLUMN";
import {
    TALLY_SHEET_CODE_CE_201,
    TALLY_SHEET_CODE_CE_201_PV,
    TALLY_SHEET_CODE_PCE_31,
    TALLY_SHEET_CODE_PCE_34,
    TALLY_SHEET_CODE_PCE_35,
    TALLY_SHEET_CODE_PCE_CE_CO_PR_4,
    TALLY_SHEET_CODE_PCE_CE_RO_V1,
    TALLY_SHEET_CODE_PCE_CE_RO_V2,
    TALLY_SHEET_CODE_PCE_R2,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_1,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_2,
    TALLY_SHEET_CODE_PCE_CE_RO_PR_3,
    TALLY_SHEET_CODE_PCE_PD_V,
    TALLY_SHEET_CODE_PCE_PC_V,
} from "./TALLY_SHEET_CODE";
import {
    VOTE_TYPE_DISPLACED,
    VOTE_TYPE_NON_POSTAL,
    VOTE_TYPE_POSTAL,
    VOTE_TYPE_POSTAL_AND_NON_POSTAL,
    VOTE_TYPE_QUARANTINE
} from "./VOTE_TYPE";

const columns_ad_pd_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_pd_cc_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION,
    TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_PARTY, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_cc_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_cc_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_COUNTING_CENTRE, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_pd_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_pd_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_POLLING_DIVISION, TALLY_SHEET_LIST_COLUMN_PARTY,
    TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_ad_party_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_ADMINISTRATIVE_DISTRICT, TALLY_SHEET_LIST_COLUMN_PARTY, TALLY_SHEET_LIST_COLUMN_STATUS,
    TALLY_SHEET_LIST_COLUMN_ACTIONS];
const columns_province_status_actions = [
    TALLY_SHEET_LIST_COLUMN_PROVINCE, TALLY_SHEET_LIST_COLUMN_STATUS, TALLY_SHEET_LIST_COLUMN_ACTIONS];

export const TALLY_SHEET_LIST_COLUMNS = {
    [TALLY_SHEET_CODE_PCE_35]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_cc_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_cc_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_cc_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_CO_PR_4]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_cc_party_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_cc_party_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_cc_party_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_cc_party_status_actions
    },
    [TALLY_SHEET_CODE_CE_201]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_cc_status_actions
    },
    [TALLY_SHEET_CODE_CE_201_PV]: {
        [VOTE_TYPE_POSTAL]: columns_ad_cc_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_cc_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_cc_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_RO_V1]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_status_actions
    },
    [TALLY_SHEET_CODE_PCE_PD_V]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_RO_PR_1]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_party_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_party_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_party_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_party_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_RO_PR_2]: {
        [VOTE_TYPE_POSTAL_AND_NON_POSTAL]: columns_ad_party_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_RO_PR_3]: {
        [VOTE_TYPE_POSTAL_AND_NON_POSTAL]: columns_ad_party_status_actions
    },
    [TALLY_SHEET_CODE_PCE_CE_RO_V2]: {
        [VOTE_TYPE_POSTAL_AND_NON_POSTAL]: columns_ad_status_actions
    },
    [TALLY_SHEET_CODE_PCE_R2]: {
        [VOTE_TYPE_POSTAL_AND_NON_POSTAL]: columns_ad_status_actions
    },
    [TALLY_SHEET_CODE_PCE_34]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_cc_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_cc_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_cc_status_actions
    },
    [TALLY_SHEET_CODE_PCE_31]: {
        [VOTE_TYPE_NON_POSTAL]: columns_ad_pd_cc_status_actions,
        [VOTE_TYPE_POSTAL]: columns_ad_cc_status_actions,
        [VOTE_TYPE_DISPLACED]: columns_ad_cc_status_actions,
        [VOTE_TYPE_QUARANTINE]: columns_ad_cc_status_actions
    },
    [TALLY_SHEET_CODE_PCE_PC_V]: {
        [VOTE_TYPE_POSTAL_AND_NON_POSTAL]: columns_province_status_actions
    }
};

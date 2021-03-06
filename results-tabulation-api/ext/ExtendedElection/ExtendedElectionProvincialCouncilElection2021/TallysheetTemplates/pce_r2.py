from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_R2, \
    PCE_CE_RO_V2
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, \
    TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED


def create_template():
    return Template.create(
        templateName=PCE_R2,
        templateRowTypesMap={
            "PARTY_WISE_VOTE": {
                "hasMany": True,
                "isDerived": True,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                ],
                "derivativeRows": [
                    {"templateName": PCE_CE_RO_V2, "templateRowType": "PARTY_WISE_VOTE"}
                ]
            },
            "REJECTED_VOTE": {
                "hasMany": True,
                "isDerived": True,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                ],
                "derivativeRows": [
                    {"templateName": PCE_CE_RO_V2, "templateRowType": "REJECTED_VOTE"}
                ]
            },
            TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            # TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED: {
            #     "hasMany": True,
            #     "isDerived": False,
            #     "columns": [
            #         {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
            #         {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
            #         {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
            #         {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
            #     ]
            # },
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            },
            # TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: {
            #     "hasMany": True,
            #     "isDerived": False,
            #     "columns": [
            #         {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
            #         {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
            #         {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
            #         {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
            #     ]
            # },
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
            }
        }
    )

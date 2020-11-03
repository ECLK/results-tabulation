from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_42, \
    PCE_PR_CD, PCE_R2, PCE_PR_PW_SA, PCE_PR_BS_1, PCE_PR_BS_2
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE


def create_template():
    return Template.create(
            templateName=PCE_PR_CD,
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
                        {"templateName": PCE_42, "templateRowType": "PARTY_WISE_VOTE"}
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
                        {"templateName": PCE_42, "templateRowType": "REJECTED_VOTE"}
                    ]
                },
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_PR_PW_SA, "templateRowType": TEMPLATE_ROW_TYPE_SEATS_ALLOCATED}
                    ]
                },
                TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_PR_BS_1, "templateRowType": TEMPLATE_ROW_TYPE_SEATS_ALLOCATED}
                    ]
                },
                TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE: {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_R2, "templateRowType": TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE},
                        {"templateName": PCE_PR_BS_2, "templateRowType": TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE}
                    ]
                }
            }
        )

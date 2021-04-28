from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_POST_PC, \
    PCE_CE_RO_V2, PCE_R2, PCE_PC_BS_1
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY, \
    TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED


def create_template():
    return Template.create(
        templateName=PCE_POST_PC,
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
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ]
                ,
                "derivativeRows": [
                    {"templateName": PCE_R2, "templateRowType": "TEMPLATE_ROW_TYPE_SEATS_ALLOCATED"}
                ]
            },
            TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                ],
                "derivativeRows": [
                    {"templateName": PCE_PC_BS_1, "templateRowType": "TEMPLATE_ROW_TYPE_SEATS_ALLOCATED"}
                ]
            }
        }
    )

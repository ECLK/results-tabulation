from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_CE_RO_V1,PCE_35
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY


def create_template():
    return Template.create(
        templateName=PCE_CE_RO_V1,
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
                    {"templateName": PCE_35, "templateRowType": "PARTY_WISE_VOTE"}
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
                    {"templateName": PCE_35, "templateRowType": "REJECTED_VOTE"}
                ]
            }
        }
    )

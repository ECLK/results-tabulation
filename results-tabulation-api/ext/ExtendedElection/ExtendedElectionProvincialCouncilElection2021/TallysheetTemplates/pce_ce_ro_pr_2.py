from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_CE_RO_PR_2, \
    PCE_CE_RO_PR_1
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY


def create_template():
    return Template.create(
        templateName=PCE_CE_RO_PR_2,
        templateRowTypesMap={
            "CANDIDATE_FIRST_PREFERENCE": {
                "hasMany": True,
                "isDerived": True,
                "columns": [
                    {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                    {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                ],
                "derivativeRows": [
                    {"templateName": PCE_CE_RO_PR_1, "templateRowType": "CANDIDATE_FIRST_PREFERENCE"}
                ]
            }
        }
    )

from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import PCE_31
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT


def create_template():
    return Template.create(
            templateName=PCE_31,
            templateRowTypesMap={
                "PARTY_WISE_INVALID_VOTE_COUNT": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "invalidVoteCategoryId", "grouped": False, "func": None,
                         "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

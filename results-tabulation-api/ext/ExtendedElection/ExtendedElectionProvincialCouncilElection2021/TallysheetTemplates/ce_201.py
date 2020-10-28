from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY


def create_template():
    return Template.create(
        templateName=CE_201,
        templateRowTypesMap={
            "BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_BALLOTS_RECEIVED": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_BALLOTS_SPOILT": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_BALLOTS_ISSUED": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_BALLOTS_UNUSED": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_PAPER_ACCOUNT": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
        }
    )

from orm.entities import Template
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201_PV
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT


def create_template():
    return Template.create(
        templateName=CE_201_PV,
        templateRowTypesMap={
            "SITUATION": {
                "hasMany": False,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "TIME_OF_COMMENCEMENT": {
                "hasMany": False,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX": {
                "hasMany": True,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A": {
                "hasMany": False,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            },
            "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B": {
                "hasMany": False,
                "isDerived": False,
                "columns": [
                    {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                    {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                ]
            }
        }
    )

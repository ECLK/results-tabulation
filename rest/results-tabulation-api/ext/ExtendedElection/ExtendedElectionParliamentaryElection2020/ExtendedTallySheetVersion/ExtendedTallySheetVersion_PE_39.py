from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheetVersion_PE_39(ExtendedTallySheetVersion):

    def __init__(self, tallySheetVersion):
        super(ExtendedTallySheetVersion_PE_39, self).__init__(tallySheetVersion)
    #
    # def html_letter(self, title="", total_registered_voters=None):
    #     # TODO: implement
    #     pass
    #
    # def html(self, title="", total_registered_voters=None):
    #     # TODO: implement
    #     pass

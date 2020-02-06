from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion


class ExtendedTallySheetVersion_PRE_AI_ED(ExtendedTallySheetVersion):

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PRE_AI_ED, self).html_letter(
            title="All Island Result - ED"
        )

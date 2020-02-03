from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion import ExtendedTallySheetVersion


class ExtendedTallySheetVersion_PRE_AI(ExtendedTallySheetVersion):

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PRE_AI, self).html_letter(
            title="All Island Result"
        )

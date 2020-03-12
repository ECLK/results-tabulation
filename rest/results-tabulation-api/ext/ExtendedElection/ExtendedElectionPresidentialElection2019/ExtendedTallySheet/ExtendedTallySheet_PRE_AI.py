from ext.ExtendedTallySheet import ExtendedTallySheet


class ExtendedTallySheet_PRE_AI(ExtendedTallySheet):
    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_PRE_AI, self).html_letter(
                title="All Island Result"
            )

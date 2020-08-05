from ext.ExtendedTallySheet import ExtendedTallySheetReport


class ExtendedTallySheet_PRE_AI(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None, signatures=[]):
            return super(ExtendedTallySheet_PRE_AI, self).html_letter(
                title="All Island Result"
            )

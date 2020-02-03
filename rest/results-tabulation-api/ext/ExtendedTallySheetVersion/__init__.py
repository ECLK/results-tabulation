def get_extended_tally_sheet_version_class(templateName):
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion import ExtendedTallySheetVersion

    EXTENDED_TEMPLATE_MAP = {
        # TODO
    }

    if templateName in EXTENDED_TEMPLATE_MAP:
        return EXTENDED_TEMPLATE_MAP[templateName]
    else:
        return ExtendedTallySheetVersion

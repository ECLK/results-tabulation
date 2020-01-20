from constants.TALLY_SHEET_CODES import PRE_ALL_ISLAND_RESULTS, PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_41, \
    PRE_30_PD, PRE_30_ED


def get_extended_tally_sheet_version_class(templateName):
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion import ExtendedTallySheetVersion
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_30_ED import ExtendedTallySheetVersion_PRE_30_ED
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_30_PD import ExtendedTallySheetVersion_PRE_30_PD
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_41 import ExtendedTallySheetVersion_PRE_41
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_AI import ExtendedTallySheetVersion_PRE_AI
    from ext.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_AI_ED import ExtendedTallySheetVersion_PRE_AI_ED

    EXTENDED_TEMPLATE_MAP = {
        PRE_41: ExtendedTallySheetVersion_PRE_41,
        PRE_30_PD: ExtendedTallySheetVersion_PRE_30_PD,
        PRE_30_ED: ExtendedTallySheetVersion_PRE_30_ED,
        PRE_ALL_ISLAND_RESULTS: ExtendedTallySheetVersion_PRE_AI,
        PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: ExtendedTallySheetVersion_PRE_AI_ED
    }

    if templateName in EXTENDED_TEMPLATE_MAP:
        return EXTENDED_TEMPLATE_MAP[templateName]
    else:
        return ExtendedTallySheetVersion

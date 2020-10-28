from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201 import \
    ExtendedTallySheet_CE_201
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201_PV import \
    ExtendedTallySheet_CE_201_PV
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_42 import \
    ExtendedTallySheet_PCE_42
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_31 import \
    ExtendedTallySheet_PCE_31
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_35 import \
    ExtendedTallySheet_PCE_35
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_34 import \
    ExtendedTallySheet_PCE_34
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_CO_PR_4 import \
    ExtendedTallySheet_PCE_CE_CO_PR_4
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_1 import \
    ExtendedTallySheet_PCE_CE_RO_PR_1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_2 import \
    ExtendedTallySheet_PCE_CE_RO_PR_2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_3 import \
    ExtendedTallySheet_PCE_CE_RO_PR_3
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V1 import \
    ExtendedTallySheet_PCE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V2 import \
    ExtendedTallySheet_PCE_CE_RO_V2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_R2 import \
    ExtendedTallySheet_PCE_R2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201, CE_201_PV, \
    PCE_31, PCE_34, PCE_35, PCE_42, PCE_CE_CO_PR_1, PCE_CE_CO_PR_2, PCE_CE_CO_PR_3, PCE_CE_CO_PR_4, PCE_CE_RO_PR_1, \
    PCE_CE_RO_PR_2, PCE_CE_RO_PR_3, PCE_CE_RO_V1, PCE_CE_RO_V2, PCE_R1, PCE_R1_PV, PCE_R2, PROVINCIAL_RESULT_CANDIDATES, \
    PROVINCIAL_RESULT_PARTY_WISE, PROVINCIAL_RESULT_PARTY_WISE_POSTAL, PROVINCIAL_RESULT_PARTY_WISE_WITH_SEATS
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021 import \
    ExtendedElectionProvincialCouncilElection2021


def get_extended_tally_sheet_class(election, templateName):
    EXTENDED_TEMPLATE_MAP = {
        CE_201: ExtendedTallySheet_CE_201,
        CE_201_PV: ExtendedTallySheet_CE_201_PV,
        PCE_31: ExtendedTallySheet_PCE_31,
        PCE_34: ExtendedTallySheet_PCE_34,
        PCE_35: ExtendedTallySheet_PCE_35,
        PCE_42: ExtendedTallySheet_PCE_42,
        PCE_CE_CO_PR_4: ExtendedTallySheet_PCE_CE_CO_PR_4,
        PCE_CE_RO_PR_1: ExtendedTallySheet_PCE_CE_RO_PR_1,
        PCE_CE_RO_PR_2: ExtendedTallySheet_PCE_CE_RO_PR_2,
        PCE_CE_RO_PR_3: ExtendedTallySheet_PCE_CE_RO_PR_3,
        PCE_CE_RO_V1: ExtendedTallySheet_PCE_CE_RO_V1,
        PCE_CE_RO_V2: ExtendedTallySheet_PCE_CE_RO_V2,
        PCE_R2: ExtendedTallySheet_PCE_R2,
        PROVINCIAL_RESULT_CANDIDATES: "",
        PROVINCIAL_RESULT_PARTY_WISE: "",
        PROVINCIAL_RESULT_PARTY_WISE_POSTAL: "",
        PROVINCIAL_RESULT_PARTY_WISE_WITH_SEATS: "",

    }

    if templateName in EXTENDED_TEMPLATE_MAP:
        return EXTENDED_TEMPLATE_MAP[templateName]
    else:
        return super(ExtendedElectionProvincialCouncilElection2021, election).get_extended_tally_sheet_class(
            templateName=templateName
        )

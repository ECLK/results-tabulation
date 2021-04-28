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
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_BS_1 import \
    ExtendedTallySheet_PCE_PC_BS_1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_BS_2 import \
    ExtendedTallySheet_PCE_PC_BS_2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_CD import \
    ExtendedTallySheet_PCE_PC_CD
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_SA_1 import \
    ExtendedTallySheet_PCE_PC_SA_1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_SA_2 import \
    ExtendedTallySheet_PCE_PC_SA_2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PC_V import \
    ExtendedTallySheet_PCE_PC_V
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_PD_V import \
    ExtendedTallySheet_PCE_PD_V
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_POST_PC import \
    ExtendedTallySheet_PCE_POST_PC
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201, CE_201_PV, \
    PCE_31, PCE_34, PCE_35, PCE_42, PCE_CE_CO_PR_1, PCE_CE_CO_PR_2, PCE_CE_CO_PR_3, PCE_CE_CO_PR_4, PCE_CE_RO_PR_1, \
    PCE_CE_RO_PR_2, PCE_CE_RO_PR_3, PCE_CE_RO_V1, PCE_CE_RO_V2, PCE_R1, PCE_R1_PV, PCE_R2, PCE_PD_V, PCE_PC_V, \
    PCE_PC_CD, PCE_PC_BS_1, PCE_PC_BS_2, PCE_PC_SA_1, PCE_PC_SA_2, PCE_POST_PC


def get_extended_tally_sheet_class(election, templateName, electionClass):
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
        PCE_PC_BS_1: ExtendedTallySheet_PCE_PC_BS_1,
        PCE_PC_BS_2: ExtendedTallySheet_PCE_PC_BS_2,
        PCE_PC_CD: ExtendedTallySheet_PCE_PC_CD,
        PCE_PC_SA_1: ExtendedTallySheet_PCE_PC_SA_1,
        PCE_PC_SA_2: ExtendedTallySheet_PCE_PC_SA_2,
        PCE_PC_V: ExtendedTallySheet_PCE_PC_V,
        PCE_PD_V: ExtendedTallySheet_PCE_PD_V,
        PCE_R2: ExtendedTallySheet_PCE_R2,
        PCE_POST_PC: ExtendedTallySheet_PCE_POST_PC
    }

    if templateName in EXTENDED_TEMPLATE_MAP:
        return EXTENDED_TEMPLATE_MAP[templateName]
    else:
        return super(electionClass, election).get_extended_tally_sheet_class(
            templateName=templateName
        )

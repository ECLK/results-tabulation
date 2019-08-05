import enum


class TallySheetInvalidVoteCategoryEnum(enum.Enum):
    HAVING_MORE_THAN = 1
    Province = 2
    AdministrativeDistrict = 3
    ElectoralDistrict = 4
    PollingDivision = 5
    PollingDistrict = 6

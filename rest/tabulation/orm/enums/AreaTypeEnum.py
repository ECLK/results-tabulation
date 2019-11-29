import enum


class AreaTypeEnum(enum.Enum):
    Country = 1
    Province = 2
    AdministrativeDistrict = 3
    ElectoralDistrict = 4
    PollingDivision = 5
    PollingDistrict = 6

    ElectionCommission = 7
    DistrictCentre = 8
    CountingCentre = 9
    PollingStation = 10

    Electorate = 11
    Office = 12
    PostalVoteCountingCentre = 13

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_increment (
    id INT AUTO_INCREMENT NOT NULL,
    active INT,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_tally_sheet_status (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    electoralDistrictId INT,
    pollingDivisionId INT,
    countingCentreId INT,
    templateName VARCHAR(50) NOT NULL,
    voteType VARCHAR(50) NOT NULL,
    partyId INT,
    verifiedTallySheetCount INT NOT NULL,
    releasedTallySheetCount INT NOT NULL,
    emptyTallySheetCount INT NOT NULL,
    savedTallySheetCount INT NOT NULL,
    totalTallySheetCount INT NOT NULL,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_party_wise_vote_results (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    electoralDistrictId INT,
    pollingDivisionId INT,
    countingCentreId INT,
    voteType VARCHAR(50) NOT NULL,
    partyId INT,
    voteCount INT,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_vote_results (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    electoralDistrictId INT,
    pollingDivisionId INT,
    countingCentreId INT,
    voteType VARCHAR(50) NOT NULL,
    validVoteCount INT,
    rejectedVoteCount INT,
    voteCount INT,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_party_wise_seat_allocation (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    electoralDistrictId INT,
    partyId INT,
    seatCount INT,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_party_wise_national_list_seat_allocation (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    partyId INT,
    nationalListSeatCount INT,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_area_map (
    id INT AUTO_INCREMENT,
    electionId INT,
    countryId INT,
    electoralDistrictId INT,
    pollingDivisionId INT,
    countingCentreId INT,
    registeredVotersCount INT,
    registeredPostalVotersCount INT,
    registeredDisplacedVotersCount INT,
    voteType VARCHAR(50) NOT NULL,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

DELETE FROM ext_pe2020_dashboard_area_map;

INSERT INTO ext_pe2020_dashboard_area_map (electionId, countryId, electoralDistrictId, pollingDivisionId,
        countingCentreId, voteType, registeredVotersCount, registeredPostalVotersCount, registeredDisplacedVotersCount)
    SELECT
        country.electionId,
        country.areaId as countryId,
        electoralDistrict.areaId as electoralDistrictId,
        pollingDivision.areaId as pollingDivisionId,
        countingCentre.areaId as countingCentreId,
        "NonPostal" as voteType,
        COALESCE(SUM(pollingStation._registeredVotersCount)) AS registeredVotersCount,
        COALESCE(SUM(pollingStation._registeredPostalVotersCount)) AS registeredPostalVotersCount,
        COALESCE(SUM(pollingStation._registeredDisplacedVotersCount)) AS registeredDisplacedVotersCount
    FROM
        area country, area electoralDistrict, area pollingDivision, area pollingDistrict, area pollingStation,
        area electionCommission, area districtCentre, area countingCentre,

        area_area country_electoralDistrict,
        area_area electoralDistrict_pollingDivision,
        area_area pollingDivision_pollingDistrict,
        area_area pollingDistrict_pollingStation,

        area_area electionCommission_districtCentre,
        area_area districtCentre_countingCentre,
        area_area countingCentre_pollingStation
    WHERE
        country_electoralDistrict.parentAreaId = country.areaId
        and country_electoralDistrict.childAreaId = electoralDistrict.areaId

        and electoralDistrict_pollingDivision.parentAreaId = electoralDistrict.areaId
        and electoralDistrict_pollingDivision.childAreaId = pollingDivision.areaId

        and pollingDivision_pollingDistrict.parentAreaId = pollingDivision.areaId
        and pollingDivision_pollingDistrict.childAreaId = pollingDistrict.areaId

        and pollingDistrict_pollingStation.parentAreaId = pollingDistrict.areaId
        and pollingDistrict_pollingStation.childAreaId = pollingStation.areaId

        and electionCommission_districtCentre.parentAreaId = electionCommission.areaId
        and electionCommission_districtCentre.childAreaId = districtCentre.areaId

        and districtCentre_countingCentre.parentAreaId = districtCentre.areaId
        and districtCentre_countingCentre.childAreaId = countingCentre.areaId

        and countingCentre_pollingStation.parentAreaId = countingCentre.areaId
        and countingCentre_pollingStation.childAreaId = pollingStation.areaId

        and country.areaType = "Country" and electoralDistrict.areaType = "ElectoralDistrict"
        and pollingDivision.areaType = "PollingDivision" and pollingDistrict.areaType = "PollingDistrict"
        and pollingStation.areaType = "PollingStation" and countingCentre.areaType = "CountingCentre"
        and districtCentre.areaType = "DistrictCentre" and electionCommission.areaType = "ElectionCommission"
    GROUP BY
        country.areaId,
        electoralDistrict.areaId,
        pollingDivision.areaId,
        countingCentre.areaId;

INSERT INTO ext_pe2020_dashboard_area_map (electionId, countryId, electoralDistrictId, pollingDivisionId,
        countingCentreId, voteType)
    SELECT
        country.electionId,
        country.areaId as countryId,
        electoralDistrict.areaId as electoralDistrictId,
        electoralDistrict.areaId as pollingDivisionId,
        countingCentre.areaId as countingCentreId,
        "Postal" AS voteType
    FROM
        area country, area electoralDistrict,
        area electionCommission, area districtCentre, area countingCentre,

        area_area country_electoralDistrict,
        area_area electoralDistrict_countingCentre,

        area_area electionCommission_districtCentre,
        area_area districtCentre_countingCentre
    WHERE
        country_electoralDistrict.parentAreaId = country.areaId
        and country_electoralDistrict.childAreaId = electoralDistrict.areaId

        and electoralDistrict_countingCentre.parentAreaId = electoralDistrict.areaId
        and electoralDistrict_countingCentre.childAreaId = countingCentre.areaId

        and electionCommission_districtCentre.parentAreaId = electionCommission.areaId
        and electionCommission_districtCentre.childAreaId = districtCentre.areaId

        and districtCentre_countingCentre.parentAreaId = districtCentre.areaId
        and districtCentre_countingCentre.childAreaId = countingCentre.areaId

        and country.areaType = "Country" and electoralDistrict.areaType = "ElectoralDistrict"
        and countingCentre.areaType = "CountingCentre" and districtCentre.areaType = "DistrictCentre"
        and electionCommission.areaType = "ElectionCommission"
    GROUP BY
        country.areaId,
        electoralDistrict.areaId,
        countingCentre.areaId;

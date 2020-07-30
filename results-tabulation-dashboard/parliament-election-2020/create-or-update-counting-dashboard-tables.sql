CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_increment (
    id INT AUTO_INCREMENT NOT NULL,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS ext_pe2020_dashboard_tally_sheet_status (
    id INT AUTO_INCREMENT,
    incrementId INT NOT NULL,
    electionId INT NOT NULL,
    electoralDistrictId INT NOT NULL,
    pollingDivisionId INT,
    countingCentreId INT NOT NULL,
    templateName VARCHAR(20) NOT NULL,
    voteType VARCHAR(20) NOT NULL,
    partyId INT,
    verifiedTallySheetCount INT NOT NULL,
    emptyTallySheetCount INT NOT NULL,
    savedTallySheetCount INT NOT NULL,
    totalTallySheetCount INT NOT NULL,
    PRIMARY KEY(id)
)  ENGINE=INNODB;

INSERT INTO ext_pe2020_dashboard_increment () VALUES();

SET @lastIncrementId = LAST_INSERT_ID();

INSERT INTO ext_pe2020_dashboard_tally_sheet_status (incrementId, electionId, electoralDistrictId, pollingDivisionId,
    countingCentreId, templateName, voteType, partyId, verifiedTallySheetCount,emptyTallySheetCount,
    savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.electoralDistrictId,
    areaMap.pollingDivisionId,
    areaMap.countingCentreId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue as "partyId",
    COUNT(IF(workflowInstance.status = "Verified", tallySheet.tallySheetId, NULL)) AS verifiedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Empty", tallySheet.tallySheetId, NULL)) AS emptyTallySheetCount,
    COUNT(IF(workflowInstance.status = "Saved", tallySheet.tallySheetId, NULL)) AS savedTallySheetCount,
    COUNT(tallySheet.tallySheetId) AS totalTallySheetCount
FROM
    (SELECT
        country.areaId as countryId,
        electoralDistrict.areaId as electoralDistrictId,
        pollingDivision.areaId as pollingDivisionId,
        countingCentre.areaId as countingCentreId,
        "NonPostal" as voteType
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
        countingCentre.areaId
    UNION SELECT
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
        countingCentre.areaId
    ) AS areaMap,
    submission, election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    submission.areaId = areaMap.countingCentreId
    and tallySheet.tallySheetId = submission.submissionId
    and election.electionId = submission.electionId
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.electoralDistrictId,
    areaMap.pollingDivisionId,
    areaMap.countingCentreId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;

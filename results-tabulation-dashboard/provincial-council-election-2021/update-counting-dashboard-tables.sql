SET @election_template_name = "PARLIAMENT_ELECTION_2020";

INSERT INTO ext_pce2021_dashboard_increment (active) VALUES(0);

SET @lastIncrementId = LAST_INSERT_ID();


INSERT INTO ext_pce2021_dashboard_tally_sheet_status (incrementId, electionId,provinceId, administrativeDistrictId, pollingDivisionId,
    countingCentreId, templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    areaMap.pollingDivisionId,
    areaMap.countingCentreId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue as "partyId",
    COUNT(IF(workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released"),
            tallySheet.tallySheetId, NULL)) AS verifiedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Released", tallySheet.tallySheetId, NULL)) AS releasedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Empty", tallySheet.tallySheetId, NULL)) AS emptyTallySheetCount,
    COUNT(IF(workflowInstance.status = "Saved", tallySheet.tallySheetId, NULL)) AS savedTallySheetCount,
    COUNT(tallySheet.tallySheetId) AS totalTallySheetCount
FROM
    ext_pce2021_dashboard_area_map AS areaMap,
    election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    tallySheet.areaId = areaMap.countingCentreId
    and election.electionId = tallySheet.electionId
    and election.electionTemplateName = @election_template_name
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    areaMap.pollingDivisionId,
    areaMap.countingCentreId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;



INSERT INTO ext_pce2021_dashboard_tally_sheet_status (incrementId, electionId, provinceId, administrativeDistrictId, pollingDivisionId,
    templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    areaMap.pollingDivisionId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue as "partyId",
    COUNT(IF(workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released"),
            tallySheet.tallySheetId, NULL)) AS verifiedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Released", tallySheet.tallySheetId, NULL)) AS releasedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Empty", tallySheet.tallySheetId, NULL)) AS emptyTallySheetCount,
    COUNT(IF(workflowInstance.status = "Saved", tallySheet.tallySheetId, NULL)) AS savedTallySheetCount,
    COUNT(tallySheet.tallySheetId) AS totalTallySheetCount
FROM
    (SELECT provinceId, administrativeDistrictId, pollingDivisionId FROM ext_pce2021_dashboard_area_map
        WHERE voteTYpe = "NonPostal" GROUP BY provinceId, administrativeDistrictId, pollingDivisionId) AS areaMap,
    election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    tallySheet.areaId = areaMap.pollingDivisionId
    and election.electionId = tallySheet.electionId
    and election.electionTemplateName = @election_template_name
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    areaMap.pollingDivisionId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;



INSERT INTO ext_pce2021_dashboard_tally_sheet_status (incrementId, electionId, provinceId,
    administrativeDistrictId, templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue as "partyId",
    COUNT(IF(workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released"),
            tallySheet.tallySheetId, NULL)) AS verifiedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Released", tallySheet.tallySheetId, NULL)) AS releasedTallySheetCount,
    COUNT(IF(workflowInstance.status = "Empty", tallySheet.tallySheetId, NULL)) AS emptyTallySheetCount,
    COUNT(IF(workflowInstance.status = "Saved", tallySheet.tallySheetId, NULL)) AS savedTallySheetCount,
    COUNT(tallySheet.tallySheetId) AS totalTallySheetCount
FROM
    (SELECT provinceId, administrativeDistrictId FROM ext_pce2021_dashboard_area_map
        WHERE voteTYpe = "NonPostal" GROUP BY provinceId, administrativeDistrictId) AS areaMap,
    election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    tallySheet.areaId = areaMap.administrativeDistrictId
    and election.electionId = tallySheet.electionId
    and election.electionTemplateName = @election_template_name
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.provinceId,
    areaMap.administrativeDistrictId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;



INSERT INTO ext_pce2021_dashboard_party_wise_vote_results (incrementId, electionId, provinceId, administrativeDistrictId,
    pollingDivisionId, countingCentreId, voteType, partyId, voteCount)
SELECT
    @lastIncrementId,
    countingCentreElection.rootElectionId AS electionId,
    province.areaId AS provinceId,
    administrativeDistrict.areaId AS administrativeDistrictId,
    pollingDivision.areaId AS pollingDivisionId,
    countingCentre.areaId AS countingCentreId,
    countingCentreElection.voteType,
    party.partyId,
    (SELECT COALESCE(SUM(tallySheetVersionRow.numValue))
        FROM tallySheet, template, templateRow, workflowInstance, tallySheetVersionRow
        WHERE
            template.templateId = tallySheet.templateId
            and templateRow.templateid = template.templateId
            and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
            and tallySheetVersionRow.tallySheetVersionId = tallySheet.latestVersionId
            and tallySheetVersionRow.templateRowId = templateRow.templateRowId
            and workflowInstance.status IN ("Verified")
            and templateRow.templateRowType = "PARTY_WISE_VOTE"
            and template.templateName = "PCE-35"
            and tallySheet.areaId = countingCentreId
            and tallySheetVersionRow.partyId = party.partyId
    ) AS voteCount
FROM ext_pce2021_dashboard_area_map AS areaMap, election_party AS electionParty, party,
         area AS countingCentre, election AS countingCentreElection, area AS pollingDivision, area AS province, area AS administrativeDistrict
WHERE
    countingCentre.areaId = areaMap.countingCentreId
    and pollingDivision.areaId = areaMap.pollingDivisionId
    and province.areaId = areaMap.provinceId
    and administrativeDistrict.areaId = areaMap.administrativeDistrictId
    and countingCentreElection.electionId = countingCentre.electionId
    and countingCentreElection.electionTemplateName = @election_template_name
    and electionParty.electionId = countingCentreElection.electionId
    and party.partyId = electionParty.partyId;



INSERT INTO ext_pce2021_dashboard_vote_results (incrementId, electionId, provinceId, administrativeDistrictId,
    pollingDivisionId, countingCentreId, voteType, validVoteCount, rejectedVoteCount, voteCount)
SELECT
    @lastIncrementId,
    countingCentreElection.rootElectionId AS electionId,
    province.areaId AS provinceId,
    administrativeDistrict.areaId AS administrativeDistrictId,
    pollingDivision.areaId AS pollingDivisionId,
    countingCentre.areaId AS countingCentreId,
    countingCentreElection.voteType,
    COALESCE(SUM(voteCounts.validVoteCount), 0),
    COALESCE(SUM(voteCounts.rejectedVoteCount), 0),
    COALESCE(SUM(voteCounts.voteCount), 0)
FROM ext_pce2021_dashboard_area_map AS areaMap,
         area AS countingCentre, election AS countingCentreElection, area AS pollingDivision, area AS province, area AS administrativeDistrict,
         (SELECT
            tallySheet.areaId AS countingCentreId,
            SUM(IF(templateRow.templateRowType = "PARTY_WISE_VOTE",tallySheetVersionRow.numValue,0)) validVoteCount,
            SUM(IF(templateRow.templateRowType = "REJECTED_VOTE",tallySheetVersionRow.numValue,0)) rejectedVoteCount,
            SUM(tallySheetVersionRow.numValue) voteCount
            FROM tallySheet, template, templateRow, workflowInstance, tallySheetVersionRow
            WHERE
                template.templateId = tallySheet.templateId
                and templateRow.templateid = template.templateId
                and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
                and tallySheetVersionRow.tallySheetVersionId = tallySheet.latestVersionId
                and tallySheetVersionRow.templateRowId = templateRow.templateRowId
                and workflowInstance.status IN ("Verified")
                and templateRow.templateRowType IN ("PARTY_WISE_VOTE", "REJECTED_VOTE")
                and template.templateName = "PCE-35"
            GROUP BY tallySheet.areaId
        ) AS voteCounts
WHERE
    countingCentre.areaId = areaMap.countingCentreId
    and pollingDivision.areaId = areaMap.pollingDivisionId
    and province.areaId = areaMap.provinceId
    and administrativeDistrict.areaId = areaMap.administrativeDistrictId
    and countingCentreElection.electionId = countingCentre.electionId
    and voteCounts.countingCentreId = countingCentre.areaId
    and countingCentreElection.electionTemplateName = @election_template_name
GROUP BY
    countingCentreElection.rootElectionId,
    province.areaId,
    administrativeDistrict.areaId,
    pollingDivision.areaId,
    countingCentre.areaId,
    countingCentreElection.voteType;



INSERT INTO ext_pce2021_dashboard_party_wise_seat_allocation (incrementId, electionId, provinceId, administrativeDistrictId, partyId, seatCount)
SELECT
    @lastIncrementId,
    administrativeDistrictElection.rootElectionId AS provinceElectionId,
    administrativeDistrict.areaId AS administrativeDistrictId,provinceElection.rootElectionId AS electionId,
    province.areaId AS provinceId,
    party.partyId,
    (SELECT COALESCE(SUM(tallySheetVersionRow.numValue), 0)
        FROM tallySheet, template, templateRow, workflowInstance, tallySheetVersionRow
        WHERE
            template.templateId = tallySheet.templateId
            and templateRow.templateid = template.templateId
            and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
            and tallySheetVersionRow.tallySheetVersionId = tallySheet.latestVersionId
            and tallySheetVersionRow.templateRowId = templateRow.templateRowId
            and workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released")
            and templateRow.templateRowType = "TEMPLATE_ROW_TYPE_SEATS_ALLOCATED"
            and template.templateName = "PCE-R2"
            and tallySheet.areaId = areaMap.administrativeDistrictId
            and tallySheetVersionRow.partyId = party.partyId
    ) AS seatCount
FROM
    (SELECT ext_pce2021_dashboard_area_map.administrativeDistrictId,ext_pce2021_dashboard_area_map.provinceId
        FROM ext_pce2021_dashboard_area_map GROUP BY ext_pce2021_dashboard_area_map.provinceId,ext_pce2021_dashboard_area_map.administrativeDistrictId) AS areaMap,
    area AS administrativeDistrict, area AS province, election AS administrativeDistrictElection, election_party AS electionParty, party
WHERE
    administrativeDistrict.areaId = areaMap.administrativeDistrictId
    and administrativeDistrictElection.electionId = administrativeDistrict.electionId
    and administrativeDistrictElection.electionTemplateName = @election_template_name
    and electionParty.electionId = administrativeDistrictElection.electionId
    and party.partyId = electionParty.partyId
GROUP BY administrativeDistrictElection.electionId, administrativeDistrict.areaId, party.partyId;



UPDATE ext_pce2021_dashboard_increment SET active = 1 WHERE id = @lastIncrementId;
DELETE FROM ext_pce2021_dashboard_tally_sheet_status WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pce2021_dashboard_party_wise_vote_results WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pce2021_dashboard_vote_results WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pce2021_dashboard_party_wise_seat_allocation WHERE incrementId < @lastIncrementId;

SET @election_template_name = "PARLIAMENT_ELECTION_2020";

INSERT INTO ext_pe2020_dashboard_increment () VALUES();

SET @lastIncrementId = LAST_INSERT_ID();


INSERT INTO ext_pe2020_dashboard_tally_sheet_status (incrementId, electionId, electoralDistrictId, pollingDivisionId,
    countingCentreId, templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.electoralDistrictId,
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
    ext_pe2020_dashboard_area_map AS areaMap,
    submission, election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    submission.areaId = areaMap.countingCentreId
    and tallySheet.tallySheetId = submission.submissionId
    and election.electionId = submission.electionId
    and election.electionTemplateName = @election_template_name
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


INSERT INTO ext_pe2020_dashboard_tally_sheet_status (incrementId, electionId, electoralDistrictId, pollingDivisionId,
    templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.electoralDistrictId,
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
    (SELECT electoralDistrictId, pollingDivisionId FROM ext_pe2020_dashboard_area_map
        WHERE voteTYpe = "NonPostal" GROUP BY electoralDistrictId, pollingDivisionId) AS areaMap,
    submission, election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    submission.areaId = areaMap.pollingDivisionId
    and tallySheet.tallySheetId = submission.submissionId
    and election.electionId = submission.electionId
    and election.electionTemplateName = @election_template_name
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.electoralDistrictId,
    areaMap.pollingDivisionId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;



INSERT INTO ext_pe2020_dashboard_tally_sheet_status (incrementId, electionId,
    electoralDistrictId, templateName, voteType, partyId, verifiedTallySheetCount, releasedTallySheetCount,
    emptyTallySheetCount, savedTallySheetCount, totalTallySheetCount)
SELECT
    @lastIncrementId,
    election.rootElectionId as electionId,
    areaMap.electoralDistrictId,
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
    (SELECT electoralDistrictId FROM ext_pe2020_dashboard_area_map
        WHERE voteTYpe = "NonPostal" GROUP BY electoralDistrictId) AS areaMap,
    submission, election, template, workflowInstance,
    tallySheet left join metaData
        on metaData.metaId = tallySheet.metaId and metaData.metaDataKey = "partyId"
WHERE
    submission.areaId = areaMap.electoralDistrictId
    and tallySheet.tallySheetId = submission.submissionId
    and election.electionId = submission.electionId
    and election.electionTemplateName = @election_template_name
    and template.templateId = tallySheet.templateId
    and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
GROUP BY
    election.rootElectionId,
    areaMap.electoralDistrictId,
    template.templateName,
    election.voteType,
    metaData.metaDataValue;
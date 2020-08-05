SET @election_template_name = "PARLIAMENT_ELECTION_2020";

INSERT INTO ext_pe2020_dashboard_increment (active) VALUES(0);

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



INSERT INTO ext_pe2020_dashboard_party_wise_vote_results (incrementId, electionId, electoralDistrictId,
    pollingDivisionId, countingCentreId, voteType, partyId, voteCount)
SELECT
    @lastIncrementId,
    countingCentreElection.rootElectionId AS electionId,
    electoralDistrict.areaId AS electoralDistrictId,
    pollingDivision.areaId AS pollingDivisionId,
    countingCentre.areaId AS countingCentreId,
    countingCentreElection.voteType,
    party.partyId,
    (SELECT COALESCE(SUM(tallySheetVersionRow.numValue))
        FROM tallySheet, submission, template, templateRow, workflowInstance, tallySheetVersionRow
        WHERE
            tallySheet.tallySheetId = submission.submissionId
            and template.templateId = tallySheet.templateId
            and templateRow.templateid = template.templateId
            and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
            and tallySheetVersionRow.tallySheetVersionId = submission.latestVersionId
            and tallySheetVersionRow.templateRowId = templateRow.templateRowId
            and workflowInstance.status IN ("Verified")
            and templateRow.templateRowType = "PARTY_WISE_VOTE"
            and template.templateName = "PE-27"
            and submission.areaId = countingCentreId
            and tallySheetVersionRow.partyId = party.partyId
    ) AS voteCount
FROM ext_pe2020_dashboard_area_map AS areaMap, election_party AS electionParty, party,
         area AS countingCentre, election AS countingCentreElection, area AS pollingDivision, area AS electoralDistrict
WHERE
    countingCentre.areaId = areaMap.countingCentreId
    and pollingDivision.areaId = areaMap.pollingDivisionId
    and electoralDistrict.areaId = areaMap.electoralDistrictId
    and countingCentreElection.electionId = countingCentre.electionId
    and countingCentreElection.electionTemplateName = @election_template_name
    and electionParty.electionId = countingCentreElection.electionId
    and party.partyId = electionParty.partyId;



INSERT INTO ext_pe2020_dashboard_vote_results (incrementId, electionId, electoralDistrictId,
    pollingDivisionId, countingCentreId, voteType, validVoteCount, rejectedVoteCount, voteCount)
SELECT
    @lastIncrementId,
    countingCentreElection.rootElectionId AS electionId,
    electoralDistrict.areaId AS electoralDistrictId,
    pollingDivision.areaId AS pollingDivisionId,
    countingCentre.areaId AS countingCentreId,
    countingCentreElection.voteType,
    COALESCE(SUM(voteCounts.validVoteCount), 0),
    COALESCE(SUM(voteCounts.rejectedVoteCount), 0),
    COALESCE(SUM(voteCounts.voteCount), 0)
FROM ext_pe2020_dashboard_area_map AS areaMap,
         area AS countingCentre, election AS countingCentreElection, area AS pollingDivision, area AS electoralDistrict,
         (SELECT
            submission.areaId AS countingCentreId,
            SUM(IF(templateRow.templateRowType = "PARTY_WISE_VOTE",tallySheetVersionRow.numValue,0)) validVoteCount,
            SUM(IF(templateRow.templateRowType = "REJECTED_VOTE",tallySheetVersionRow.numValue,0)) rejectedVoteCount,
            SUM(tallySheetVersionRow.numValue) voteCount
            FROM tallySheet, submission, template, templateRow, workflowInstance, tallySheetVersionRow
            WHERE
                tallySheet.tallySheetId = submission.submissionId
                and template.templateId = tallySheet.templateId
                and templateRow.templateid = template.templateId
                and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
                and tallySheetVersionRow.tallySheetVersionId = submission.latestVersionId
                and tallySheetVersionRow.templateRowId = templateRow.templateRowId
                and workflowInstance.status IN ("Verified")
                and templateRow.templateRowType IN ("PARTY_WISE_VOTE", "REJECTED_VOTE")
                and template.templateName = "PE-27"
            GROUP BY submission.areaId
        ) AS voteCounts
WHERE
    countingCentre.areaId = areaMap.countingCentreId
    and pollingDivision.areaId = areaMap.pollingDivisionId
    and electoralDistrict.areaId = areaMap.electoralDistrictId
    and countingCentreElection.electionId = countingCentre.electionId
    and voteCounts.countingCentreId = countingCentre.areaId
    and countingCentreElection.electionTemplateName = @election_template_name
GROUP BY
    countingCentreElection.rootElectionId,
    electoralDistrict.areaId,
    pollingDivision.areaId,
    countingCentre.areaId,
    countingCentreElection.voteType;



INSERT INTO ext_pe2020_dashboard_party_wise_seat_allocation (incrementId, electionId, electoralDistrictId, partyId, seatCount)
SELECT
    @lastIncrementId,
    electoralDistrictElection.rootElectionId AS electionId,
    electoralDistrict.areaId AS electoralDistrictId,
    party.partyId,
    (SELECT COALESCE(SUM(tallySheetVersionRow.numValue), 0)
        FROM tallySheet, submission, template, templateRow, workflowInstance, tallySheetVersionRow
        WHERE
            tallySheet.tallySheetId = submission.submissionId
            and template.templateId = tallySheet.templateId
            and templateRow.templateid = template.templateId
            and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
            and tallySheetVersionRow.tallySheetVersionId = submission.latestVersionId
            and tallySheetVersionRow.templateRowId = templateRow.templateRowId
            and workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released")
            and templateRow.templateRowType = "TEMPLATE_ROW_TYPE_SEATS_ALLOCATED"
            and template.templateName = "PE-R2"
            and submission.areaId = areaMap.electoralDistrictId
            and tallySheetVersionRow.partyId = party.partyId
    ) AS seatCount
FROM
    (SELECT ext_pe2020_dashboard_area_map.electoralDistrictId
        FROM ext_pe2020_dashboard_area_map GROUP BY ext_pe2020_dashboard_area_map.electoralDistrictId) AS areaMap,
    area AS electoralDistrict, election AS electoralDistrictElection, election_party AS electionParty, party
WHERE
    electoralDistrict.areaId = areaMap.electoralDistrictId
    and electoralDistrictElection.electionId = electoralDistrict.electionId
    and electoralDistrictElection.electionTemplateName = @election_template_name
    and electionParty.electionId = electoralDistrictElection.electionId
    and party.partyId = electionParty.partyId
GROUP BY electoralDistrictElection.electionId, electoralDistrict.areaId, party.partyId;



INSERT INTO ext_pe2020_dashboard_party_wise_national_list_seat_allocation(incrementId, electionId, partyId,
        nationalListSeatCount)
SELECT
    @lastIncrementId,
    election.electionId AS electionId,
    party.partyId,
    (SELECT COALESCE(SUM(tallySheetVersionRow.numValue), 0)
        FROM tallySheet, submission, template, templateRow, workflowInstance, tallySheetVersionRow
        WHERE
            tallySheet.tallySheetId = submission.submissionId
            and template.templateId = tallySheet.templateId
            and templateRow.templateid = template.templateId
            and workflowInstance.workflowInstanceId = tallySheet.workflowInstanceId
            and tallySheetVersionRow.tallySheetVersionId = submission.latestVersionId
            and tallySheetVersionRow.templateRowId = templateRow.templateRowId
            and workflowInstance.status IN ("Verified", "Ready to Certify", "Certified", "Release Notified", "Released")
            and templateRow.templateRowType = "TEMPLATE_ROW_TYPE_SEATS_ALLOCATED"
            and template.templateName = "PE-AI-NL-1"
            and submission.electionId = election.electionId
            and tallySheetVersionRow.partyId = party.partyId
    ) AS nationalListSeatCount
FROM
    election, election_party AS electionParty, party
WHERE
    election.electionId = election.rootElectionId
    and election.electionTemplateName = @election_template_name
    and electionParty.electionId = election.electionId
    and party.partyId = electionParty.partyId
GROUP BY election.electionId, party.partyId;



UPDATE ext_pe2020_dashboard_increment SET active = 1 WHERE id = @lastIncrementId;
DELETE FROM ext_pe2020_dashboard_tally_sheet_status WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pe2020_dashboard_party_wise_vote_results WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pe2020_dashboard_vote_results WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pe2020_dashboard_party_wise_seat_allocation WHERE incrementId < @lastIncrementId;
DELETE FROM ext_pe2020_dashboard_party_wise_national_list_seat_allocation WHERE incrementId < @lastIncrementId;

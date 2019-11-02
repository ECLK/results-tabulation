from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_, or_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_34_CO_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_CO_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_CO
    }

    def add_row(self, preferenceNumber, preferenceCount, candidateId, electionId):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference

        TallySheetVersionRow_PRE_34_preference.create(
            tallySheetVersionId=self.tallySheetVersionId,
            electionId=electionId,
            preferenceNumber=preferenceNumber,
            preferenceCount=preferenceCount,
            candidateId=candidateId
        )

    @hybrid_property
    def content(self):

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber,
            TallySheetVersionRow_PRE_34_preference.Model.preferenceCount,
            TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId,
            TallySheetVersionRow_PRE_34_preference.Model.electionId
        ).join(
            TallySheetVersionRow_PRE_34_preference.Model,
            and_(
                TallySheetVersionRow_PRE_34_preference.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId == self.tallySheetVersionId,
            ),
            isouter=True
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
            isouter=True
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId,
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId.in_(self.submission.election.mappedElectionIds),
            ElectionCandidate.Model.qualifiedForPreferences == True
        ).all()

    def html(self):
        stamp = self.stamp
        tallySheetContent = self.content

        polling_divisions = Area.get_associated_areas(self.submission.area, AreaTypeEnum.PollingDivision)
        polling_division_name = ""
        if len(polling_divisions) > 0:
            polling_division_name = polling_divisions[0].areaName

        disqualifiedCandidates = db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).filter(
            ElectionCandidate.Model.qualifiedForPreferences == False,
            ElectionCandidate.Model.electionId.in_(self.submission.election.mappedElectionIds)
        ).all()

        content = {
            "election": {
                "electionName": self.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": polling_division_name,
            "countingCentre": self.submission.area.areaName,
            "pollingDistrictNos": ", ".join([
                pollingDistrict.areaName for pollingDistrict in
                Area.get_associated_areas(self.submission.area, AreaTypeEnum.PollingDistrict)
            ]),
            "data": [],
            "candidates": disqualifiedCandidates
        }

        temp_data = {}

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.preferenceCount is not None:
                temp_data[row.candidateId] = {}

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.preferenceCount is not None:

                if row.preferenceNumber == 2:
                    preference = "secondPreferenceCount"
                elif row.preferenceNumber == 3:
                    preference = "thirdPreferenceCount"
                else:
                    preference = ""

                temp_data[row.candidateId]['name'] = row.candidateName
                temp_data[row.candidateId][preference] = row.preferenceCount

        for i in temp_data:
            content['data'].append(temp_data[i])

        html = render_template(
            'PRE-34-CO.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_34_CO_Model

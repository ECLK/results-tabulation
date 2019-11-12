from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_, or_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference, \
    TallySheetVersionRow_PRE_34_summary
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_34_I_RO_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_I_RO_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_I_RO
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
        summary = db.session.query(
            TallySheetVersionRow_PRE_34_summary.Model.ballotPapersNotCounted,
            TallySheetVersionRow_PRE_34_summary.Model.remainingBallotPapers,
        ).filter(
            TallySheetVersionRow_PRE_34_summary.Model.tallySheetVersionId == self.tallySheetVersionId
        ).one_or_none()

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
            "tallySheetCode": "PRE/34/I/RO",
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
            "pollingDivisionOrPostalVoteCountingCentres": "XX",
            "data": [],
            "candidates": disqualifiedCandidates,
            "summary": summary
        }

        if self.submission.election.voteType == VoteTypeEnum.Postal:
            content["tallySheetCode"] = "PRE/34/I/RO PV"
            content["pollingDivisionOrPostalVoteCountingCentres"] = ", ".join([
                countingCentre.areaName for countingCentre in
                Area.get_associated_areas(self.submission.area, AreaTypeEnum.CountingCentre,
                                          electionId=self.submission.electionId)
            ])
        elif self.submission.election.voteType == VoteTypeEnum.NonPostal:
            content["pollingDivisionOrPostalVoteCountingCentres"] = Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.PollingDivision)[0].areaName

        content["data"] = TallySheetVersion.create_candidate_preference_struct(self.content)

        html = render_template(
            'PRE-34-I-RO.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_34_I_RO_Model

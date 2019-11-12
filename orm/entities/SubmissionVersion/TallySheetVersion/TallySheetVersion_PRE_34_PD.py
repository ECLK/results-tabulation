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
from datetime import datetime


class TallySheetVersion_PRE_34_PD_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_PD_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_PD
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
            TallySheetVersionRow_PRE_34_preference.Model.electionId,
            Party.Model.partyAbbreviation,
            Party.Model.partyName
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

    def html_letter(self):

        stamp = self.stamp

        content = {
            "election": {
                "electionName": self.submission.election.get_official_name(),
                "isPostal": self.submission.election.voteType == VoteTypeEnum.Postal
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "date": stamp.createdAt.strftime("%d/%m/%Y"),
            "time": stamp.createdAt.strftime("%H:%M:%S %p"),
            "data": [
            ],
            "validVoteCounts": [0, 0],
            "rejectedVoteCounts": [0, 0],
            "totalVoteCounts": [0, 0],
            "registeredVoters": [
                to_comma_seperated_num(self.submission.area.registeredVotersCount),
                100
            ],
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": self.submission.area.areaName
        }

        content["data"] = TallySheetVersion.create_candidate_preference_struct(self.content)

        html = render_template(
            'PRE-34-PD-LETTER.html',
            content=content
        )

        return html

    def html(self):
        stamp = self.stamp

        content = {
            "tallySheetCode": "PRE-34-PD",
            "election": {
                "electionName": self.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": "XX",
            "data": [],
            # "candidates": disqualifiedCandidates
        }

        if self.submission.election.voteType == VoteTypeEnum.Postal:
            content["tallySheetCode"] = "PRE-34-PV"
            content["pollingDivision"] = "Postal"
        elif self.submission.election.voteType == VoteTypeEnum.NonPostal:
            content["pollingDivision"] = self.submission.area.areaName

        content["data"] = TallySheetVersion.create_candidate_preference_struct(self.content)

        html = render_template(
            'PRE-34-PD.html',
            content=content
        )

        return html

    def json_data(self):

        electoral_district = Area.get_associated_areas(self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName
        polling_division = self.submission.area.areaName
        candidate_wise_vote_count_result = TallySheetVersion.create_candidate_preference_struct(self.content)

        candidates = []
        vote_count_result = self.vote_count_query().one_or_none()
        total_valid_votes = vote_count_result.validVoteCount or 0
        for candidate_wise_valid_vote_count_result_item in candidate_wise_vote_count_result:
            total_vote_count = candidate_wise_valid_vote_count_result_item['total']
            candidates.append({
                "party_code": candidate_wise_valid_vote_count_result_item['partyAbbreviation'],
                "votes": str(total_vote_count),
                "votes1st": str(candidate_wise_valid_vote_count_result_item['firstPreferenceCount']),
                "votes2nd": str(candidate_wise_valid_vote_count_result_item['secondPreferenceCount']),
                "votes3rd": str(candidate_wise_valid_vote_count_result_item['thirdPreferenceCount']),
                "percentage": f'{round(total_vote_count*100/total_valid_votes,2)}',
                "party_name": candidate_wise_valid_vote_count_result_item['partyName'],
                "candidate": candidate_wise_valid_vote_count_result_item['name']
            })

        is_postal = self.submission.election.voteType == VoteTypeEnum.Postal
        ed_name = electoral_district.split(" - ")[1]
        ed_code = electoral_district.split(" - ")[0]
        if is_postal:
            pd_name = "Postal Votes"
            pd_code = ed_code + 'P'
        else:
            pd_name = polling_division.split("- ")[1]
            pd_code = ed_code + polling_division.split("- ")[0]

        response = {
            "timestamp": str(datetime.now()),
            "level": "POLLING-DIVISION",
            "ed_code": ed_code,
            "ed_name": ed_name,
            "pd_code": pd_code,
            "pd_name": pd_name,
            "by_party": candidates,
            "summary": {
                "valid": str(total_valid_votes),
                "rejected": "",
                "polled": "",
                "electors": "",
                "percent_valid": "",
                "percent_rejected": "",
                "percent_polled": "",
            }
        }

        return response, pd_code


Model = TallySheetVersion_PRE_34_PD_Model

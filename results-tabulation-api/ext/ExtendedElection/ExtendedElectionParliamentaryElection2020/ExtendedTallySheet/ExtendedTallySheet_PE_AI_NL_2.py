from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_PE_AI_NL_2_CANNOT_BE_PROCESSED_WITHOUT_PE_AI_NL_1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import CANDIDATE_TYPE_NATIONAL_LIST

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Election.ElectionCandidate import ElectionCandidateModel
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
from orm.entities import Candidate
from util import convert_image_to_data_uri


class ExtendedTallySheet_PE_AI_NL_2(ExtendedEditableTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):

        def get_post_save_request_content(self):
            tally_sheet_id = self.tallySheetVersion.tallySheetId

            template_rows = db.session.query(
                TemplateRowModel.templateRowId,
                TemplateRowModel.templateRowType
            ).filter(
                TemplateModel.templateId == TallySheet.Model.templateId,
                TemplateRowModel.templateId == TemplateModel.templateId,
                TemplateRowModel.templateRowType.in_([
                    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
                    TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
                ]),
                TallySheet.Model.tallySheetId == tally_sheet_id
            ).group_by(
                TemplateRowModel.templateRowId
            ).all()

            content = []

            seats_allocated_per_party_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED) & (self.df['numValue'] > 0)]

            if len(seats_allocated_per_party_df) == 0:
                raise ForbiddenException(
                    message="National list candidates cannot be allocated until the national vote calculation (PE-AI-ED) is completed and verified.",
                    code=MESSAGE_CODE_PE_AI_NL_2_CANNOT_BE_PROCESSED_WITHOUT_PE_AI_NL_1
                )

            # The derived rows are calculated only if the PE-R2 is available and verified.
            if len(seats_allocated_per_party_df) > 0:
                for index_1 in seats_allocated_per_party_df.index:
                    party_id = int(seats_allocated_per_party_df.at[index_1, "partyId"])
                    number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]

                    if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):

                        candidates = db.session.query(Candidate.Model.candidateId).filter(
                            Candidate.Model.candidateId == ElectionCandidateModel.candidateId,
                            Candidate.Model.candidateType == CANDIDATE_TYPE_NATIONAL_LIST,
                            ElectionCandidateModel.partyId == party_id
                        ).group_by(Candidate.Model.candidateId).order_by(Candidate.Model.candidateId).all()

                        for candidate in candidates:
                            if number_of_seats_allocated > 0:
                                for template_row in template_rows:
                                    candidate_id = candidate.candidateId
                                    content.append({
                                        "templateRowId": template_row.templateRowId,
                                        "templateRowType": template_row.templateRowType,
                                        "partyId": int(party_id),
                                        "candidateId": int(candidate_id),

                                        # TODO remove once the complete validation has been fixed.
                                        "numValue": 0
                                    })

                                number_of_seats_allocated -= 1

            return content

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "data": [],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            elected_candidates_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE) & (self.df['numValue'] == 0)]

            elected_candidates_df = elected_candidates_df.sort_values(
                by=['partyId', 'candidateId'], ascending=True
            )

            for index in elected_candidates_df.index:
                party_name = elected_candidates_df.at[index, "partyName"]
                party_abbreviation = elected_candidates_df.at[index, "partyAbbreviation"]
                candidate_number = elected_candidates_df.at[index, "candidateNumber"]
                candidate_name = elected_candidates_df.at[index, "candidateName"]
                content["data"].append([
                    party_name,
                    party_abbreviation,
                    "" if candidate_number is None else candidate_number,
                    "" if candidate_name is None else candidate_name
                ])

            html = render_template(
                'ParliamentaryElection2020/PE-AI-NL-2.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "data": [],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            elected_candidates_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE) & (self.df['numValue'] == 0)]

            elected_candidates_df = elected_candidates_df.sort_values(
                by=['partyId', 'candidateId'], ascending=True
            )

            for index in elected_candidates_df.index:
                party_name = elected_candidates_df.at[index, "partyName"]
                party_abbreviation = elected_candidates_df.at[index, "partyAbbreviation"]
                candidate_number = elected_candidates_df.at[index, "candidateNumber"]
                candidate_name = elected_candidates_df.at[index, "candidateName"]
                content["data"].append([
                    party_name,
                    party_abbreviation,
                    "" if candidate_number is None else candidate_number,
                    "" if candidate_name is None else candidate_name
                ])

            html = render_template(
                'ParliamentaryElection2020/PE-AI-NL-2-LETTER.html',
                content=content
            )

            return html

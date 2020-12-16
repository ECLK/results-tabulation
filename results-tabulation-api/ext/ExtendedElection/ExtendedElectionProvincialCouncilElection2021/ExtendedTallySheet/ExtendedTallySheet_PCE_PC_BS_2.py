from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_PCE_PC_BS_2_CANNOT_BE_PROCESSED_WITHOUT_PCE_PC_BS_1

from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Election.ElectionCandidate import ElectionCandidateModel
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
from orm.entities import Candidate, TallySheet
from util import convert_image_to_data_uri


class ExtendedTallySheet_PCE_PC_BS_2(ExtendedEditableTallySheetReport):
    def on_get_release_result_params(self):
        pd_code = None
        pd_name = None
        ed_code = None
        ed_name = None

        result_type = "RN_NC"
        result_code = "FINAL"
        result_level = "PROVINCE"

        return result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name

    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):
        def json(self):
            extended_tally_sheet = self.tallySheet.get_extended_tally_sheet()
            result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = extended_tally_sheet.on_get_release_result_params()

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=['electionPartyId', "candidateId"], ascending=[True, True]
            ).reset_index()

            return {
                "type": result_type,
                "level": result_level,
                "by_candidate": [
                    {
                        "party_code": candidate_wise_result.partyAbbreviation,
                        "party_name": candidate_wise_result.partyName,
                        "candidate_number": str(candidate_wise_result.candidateNumber),
                        "candidate_name": candidate_wise_result.candidateName,
                        "candidate_type": candidate_wise_result.candidateType
                    } for candidate_wise_result in candidate_wise_results.itertuples()
                ]
            }

        def get_candidate_wise_results(self):
            candidate_wise_results = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE) & (self.df['numValue'] == 0)]

            candidate_wise_results = candidate_wise_results.sort_values(
                by=['electionPartyId', 'candidateId'], ascending=True
            )

            return candidate_wise_results

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
                    message="Bonus Seat Allocation 2 (PCE_PC_BS_2) cannot be determined until the Bonus Seat Allocation 1 (PCE_PC_BS_1) is decided and verified.",
                    code=MESSAGE_CODE_PCE_PC_BS_2_CANNOT_BE_PROCESSED_WITHOUT_PCE_PC_BS_1
                )

            # The derived rows are calculated only if the PCE-R2 is available and verified.
            if len(seats_allocated_per_party_df) > 0:
                for index_1 in seats_allocated_per_party_df.index:
                    party_id = int(seats_allocated_per_party_df.at[index_1, "partyId"])
                    number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]

                    if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):

                        candidates = db.session.query(Candidate.Model.candidateId).filter(
                            Candidate.Model.candidateId == ElectionCandidateModel.candidateId,
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
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name(),
                    "provinceName": tallySheetVersion.tallySheet.area.areaName
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

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=['electionPartyId', "candidateId"], ascending=[True, True]
            ).reset_index()

            for candidate_wise_result in candidate_wise_results.itertuples():
                party_name = candidate_wise_result.partyName
                party_abbreviation = candidate_wise_result.partyAbbreviation
                candidate_number = candidate_wise_result.candidateNumber
                candidate_name = candidate_wise_result.candidateName
                content["data"].append([
                    party_name,
                    party_abbreviation,
                    "" if candidate_number is None else candidate_number,
                    "" if candidate_name is None else candidate_name
                ])

            html = render_template(
                'ProvincialCouncilElection2021/PCE-PC-BS-2.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None, signatures=[]):
            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name(),
                    "provinceName": tallySheetVersion.tallySheet.area.areaName
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "signatures": signatures,
                "data": [],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=['electionPartyId', "candidateId"], ascending=[True, True]
            ).reset_index()

            for candidate_wise_result in candidate_wise_results.itertuples():
                party_name = candidate_wise_result.partyName
                party_abbreviation = candidate_wise_result.partyAbbreviation
                candidate_number = candidate_wise_result.candidateNumber
                candidate_name = candidate_wise_result.candidateName
                content["data"].append([
                    party_name,
                    party_abbreviation,
                    "" if candidate_number is None else candidate_number,
                    "" if candidate_name is None else candidate_name
                ])

            html = render_template(
                'ProvincialCouncilElection2021/PCE-PC-BS-2-LETTER.html',
                content=content
            )

            return html

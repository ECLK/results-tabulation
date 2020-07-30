from flask import render_template

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import CANDIDATE_TYPE_NATIONAL_LIST
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from util import convert_image_to_data_uri


class ExtendedTallySheet_PE_AI_2(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):
        def get_elected_candidates(self):
            elected_candidates = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE) & (self.df['numValue'] == 0)]

            elected_candidates = elected_candidates.sort_values(
                by=['partyId', 'candidateId'], ascending=True
            ).reset_index()

            return elected_candidates

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

            elected_candidates = self.get_elected_candidates()

            for elected_candidate in elected_candidates.itertuples():
                data_row = [
                    elected_candidate.partyName,
                    elected_candidate.partyAbbreviation,
                    "National List" if elected_candidate.candidateType == CANDIDATE_TYPE_NATIONAL_LIST else elected_candidate.areaName,
                    elected_candidate.candidateNumber,
                    elected_candidate.candidateName
                ]

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-2.html',
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

            elected_candidates = self.get_elected_candidates()

            for elected_candidate in elected_candidates.itertuples():
                data_row = [
                    elected_candidate.partyName,
                    elected_candidate.partyAbbreviation,
                    "National List" if elected_candidate.candidateType == CANDIDATE_TYPE_NATIONAL_LIST else elected_candidate.areaName,
                    elected_candidate.candidateNumber,
                    elected_candidate.candidateName
                ]

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-2-LETTER.html',
                content=content
            )

            return html

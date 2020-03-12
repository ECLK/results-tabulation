from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_22(ExtendedTallySheet):
    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):

        def __init__(self, tallySheetVersion):
            super(ExtendedTallySheet_PE_22.ExtendedTallySheetVersion, self).__init__(tallySheetVersion)

        #
        # def html_letter(self, title="", total_registered_voters=None):
        #     # TODO: implement
        #     pass
        #
        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            party_wise_invalid_vote_category_counts = self.get_party_wise_invalid_vote_category_count()

            stamp = tallySheetVersion.stamp

            polling_divisions = Area.get_associated_areas(tallySheetVersion.submission.area,
                                                          AreaTypeEnum.PollingDivision)
            polling_division_name = ""
            if len(polling_divisions) > 0:
                polling_division_name = polling_divisions[0].areaName

            if tallySheetVersion.submission.election.voteType == Postal:
                polling_division_name = 'Postal'

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PE-39",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "partyWiseData": [],
                "reasonWiseTotal": [],
                "totalRejectedVotes": 0
            }

            invalid_vote_category_ids = []
            party_id_to_name = {}
            party_to_invalid_vote_category_to_count = {}
            total_rejected_count = 0
            for index, party_wise_invalid_vote_category_count in party_wise_invalid_vote_category_counts.iterrows():
                party_id = party_wise_invalid_vote_category_count.partyId
                invalid_vote_category_id = party_wise_invalid_vote_category_count.invalidVoteCategoryId
                num_value = party_wise_invalid_vote_category_count.numValue

                invalid_vote_category_ids.append(invalid_vote_category_id)
                party_id_to_name[party_id] = party_wise_invalid_vote_category_count.partyName
                if party_id not in party_to_invalid_vote_category_to_count.keys():
                    party_to_invalid_vote_category_to_count[party_id] = {}

                party_to_invalid_vote_category_to_count[party_id][invalid_vote_category_id] = num_value

            sorted_invalid_vote_category_ids = sorted(set(invalid_vote_category_ids))
            for party_id in sorted(party_to_invalid_vote_category_to_count.keys()):
                data_row = []
                data_row.append(party_id_to_name[party_id])
                party_wise_total = 0;
                for invalid_vote_category_id in sorted_invalid_vote_category_ids:
                    vote_count = 0
                    if invalid_vote_category_id in party_to_invalid_vote_category_to_count[party_id].keys():
                        vote_count = party_to_invalid_vote_category_to_count[party_id][invalid_vote_category_id]
                    data_row.append(vote_count)
                    party_wise_total += vote_count
                total_rejected_count += party_wise_total
                data_row.append(party_wise_total)
                content["partyWiseData"].append(data_row)
            content["totalRejectedVotes"] = to_comma_seperated_num(total_rejected_count)

            html = render_template(
                'PE-22.html',
                content=content
            )

            return html

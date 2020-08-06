from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_PE_AI_NL_1_CANNOT_BE_PROCESSED_WITHOUT_PE_AI_ED
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
from flask import render_template
from util import to_comma_seperated_num, convert_image_to_data_uri, to_percentage
import math
import pandas as pd
import numpy as np

template_row_to_df_num_value_column_map = {
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: "seatsAllocatedFromRound1",
    TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: "validVotesRemainFromRound1",
    TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: "draftSeatsAllocatedFromRound2",
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: "seatsAllocatedFromRound2",
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: "seatsAllocated",
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: "voteCountCeilPerSeat"
}


class ExtendedTallySheet_PE_AI_NL_1(ExtendedEditableTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):

        def get_post_save_request_content(self):
            tally_sheet_id = self.tallySheetVersion.tallySheetId
            number_of_members_to_be_elected = 29

            df = self.populate_seats_per_party(number_of_members_to_be_elected=number_of_members_to_be_elected)

            template_row_map = {
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: [],
                TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: [],
                TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: [],
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: [],
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: [],
                TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: []
            }

            for templateRowType in template_row_to_df_num_value_column_map.keys():
                template_row_map[templateRowType] = db.session.query(
                    TemplateRowModel.templateRowId
                ).filter(
                    TemplateModel.templateId == TallySheet.Model.templateId,
                    TemplateRowModel.templateId == TemplateModel.templateId,
                    TemplateRowModel.templateRowType == templateRowType,
                    TallySheet.Model.tallySheetId == tally_sheet_id
                ).group_by(
                    TemplateRowModel.templateRowId
                ).all()

            content = []

            for index in df.index:
                for templateRowType in template_row_to_df_num_value_column_map.keys():
                    for templateRow in template_row_map[templateRowType]:
                        content.append({
                            "templateRowId": templateRow.templateRowId,
                            "templateRowType": templateRowType,
                            "partyId": int(df.at[index, "partyId"]),
                            "numValue": float(df.at[index, template_row_to_df_num_value_column_map[templateRowType]])
                        })

            return content

        def populate_seats_per_party(self, number_of_members_to_be_elected=0):
            df = self.get_party_wise_valid_vote_count_result()

            total_valid_vote_count = df['numValue'].sum()

            if total_valid_vote_count == 0:
                raise ForbiddenException(
                    message="National list seat calculation cannot be done on zero votes.",
                    code=MESSAGE_CODE_PE_AI_NL_1_CANNOT_BE_PROCESSED_WITHOUT_PE_AI_ED
                )

            valid_vote_count_required_per_seat = total_valid_vote_count / number_of_members_to_be_elected
            valid_vote_count_required_per_seat_ceil = math.ceil(valid_vote_count_required_per_seat)

            for index in df.index:
                num_value = df.at[index, 'numValue']
                number_of_seats_qualified = math.floor(num_value / valid_vote_count_required_per_seat_ceil)
                df.at[index, 'seatsAllocatedFromRound1'] = number_of_seats_qualified
                number_of_members_to_be_elected -= number_of_seats_qualified
                df.at[index, 'validVotesRemainFromRound1'] = num_value % valid_vote_count_required_per_seat_ceil

            df = df.sort_values(by=['validVotesRemainFromRound1'], ascending=False)
            for index in df.index:
                if number_of_members_to_be_elected > 0:
                    number_of_seats_qualified = 1
                    df.at[index, 'seatsAllocatedFromRound2'] = number_of_seats_qualified
                    number_of_members_to_be_elected -= number_of_seats_qualified
                else:
                    df.at[index, 'seatsAllocatedFromRound2'] = 0

            df['seatsAllocated'] = df.seatsAllocatedFromRound1 + df.seatsAllocatedFromRound2

            df['draftSeatsAllocatedFromRound2'] = df.seatsAllocatedFromRound2

            df = df.sort_values(by=['numValue'], ascending=False)

            df["voteCountCeilPerSeat"] = pd.Series(
                np.full(len(df.index), valid_vote_count_required_per_seat_ceil),
                index=df.index)

            return df

        def get_party_wise_seat_calculations(self):
            party_wise_calculations_df = self.get_party_wise_valid_vote_count_result()

            for template_row_type in template_row_to_df_num_value_column_map:
                df_column_name = template_row_to_df_num_value_column_map[template_row_type]
                party_wise_calculations_df[df_column_name] = pd.Series(
                    np.zeros(len(party_wise_calculations_df.index)),
                    index=party_wise_calculations_df.index
                )

            for index_1 in party_wise_calculations_df.index:
                party_id = party_wise_calculations_df.at[index_1, "partyId"]
                filtered_df = self.df.loc[self.df['partyId'] == party_id]

                for index_2 in filtered_df.index:
                    template_row_type = filtered_df.at[index_2, "templateRowType"]
                    num_value = filtered_df.at[index_2, "numValue"]
                    if template_row_type in template_row_to_df_num_value_column_map:
                        df_column_name = template_row_to_df_num_value_column_map[template_row_type]
                        party_wise_calculations_df.at[index_1, df_column_name] += num_value

            party_wise_calculations_df = party_wise_calculations_df.sort_values(
                by=['seatsAllocated', "numValue", "electionPartyId"], ascending=[False, False, True]
            )

            return party_wise_calculations_df

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_seat_calculations()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count()
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
                "validVoteCounts": [0, "0%"],
                "rejectedVoteCounts": [0, "0%"],
                "totalVoteCounts": [0, "0%"],
                "registeredVoters": [
                    to_comma_seperated_num(registered_voters_count),
                    100
                ],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            total_valid_vote_count = 0
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                total_valid_vote_count += float(area_wise_valid_vote_count_result_item.incompleteNumValue)
            content["validVoteCounts"][0] = to_comma_seperated_num(total_valid_vote_count)
            content["validVoteCounts"][1] = to_percentage((total_valid_vote_count / registered_voters_count) * 100)

            total_rejected_vote_count = 0
            for area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.itertuples():
                total_rejected_vote_count += float(area_wise_rejected_vote_count_result_item.numValue)
            content["rejectedVoteCounts"][0] = to_comma_seperated_num(total_rejected_vote_count)
            content["rejectedVoteCounts"][1] = to_percentage(
                (total_rejected_vote_count / registered_voters_count) * 100)

            total_vote_count = 0
            for area_wise_vote_count_result_item in area_wise_vote_count_result.itertuples():
                total_vote_count += float(area_wise_vote_count_result_item.incompleteNumValue)
            content["totalVoteCounts"][0] = to_comma_seperated_num(total_vote_count)
            content["totalVoteCounts"][1] = to_percentage((total_vote_count / registered_voters_count) * 100)

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():

                data_row = [
                    party_wise_valid_vote_count_result_item.partyName,
                    party_wise_valid_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(party_wise_valid_vote_count_result_item.numValue)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_valid_vote_count_result_item.numValue * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.seatsAllocated))

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-NL-1.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None, signatures=[]):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_seat_calculations()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count()
            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "signatures": signatures,
                "data": [],
                "validVoteCounts": [0, "0%"],
                "rejectedVoteCounts": [0, "0%"],
                "totalVoteCounts": [0, "0%"],
                "registeredVoters": [
                    to_comma_seperated_num(registered_voters_count),
                    100
                ],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            total_valid_vote_count = 0
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                total_valid_vote_count += float(area_wise_valid_vote_count_result_item.incompleteNumValue)
            content["validVoteCounts"][0] = to_comma_seperated_num(total_valid_vote_count)
            content["validVoteCounts"][1] = to_percentage((total_valid_vote_count / registered_voters_count) * 100)

            total_rejected_vote_count = 0
            for area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.itertuples():
                total_rejected_vote_count += float(area_wise_rejected_vote_count_result_item.numValue)
            content["rejectedVoteCounts"][0] = to_comma_seperated_num(total_rejected_vote_count)
            content["rejectedVoteCounts"][1] = to_percentage(
                (total_rejected_vote_count / registered_voters_count) * 100)

            total_vote_count = 0
            for area_wise_vote_count_result_item in area_wise_vote_count_result.itertuples():
                total_vote_count += float(area_wise_vote_count_result_item.incompleteNumValue)
            content["totalVoteCounts"][0] = to_comma_seperated_num(total_vote_count)
            content["totalVoteCounts"][1] = to_percentage((total_vote_count / registered_voters_count) * 100)

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():

                data_row = [
                    party_wise_valid_vote_count_result_item.partyName,
                    party_wise_valid_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(party_wise_valid_vote_count_result_item.numValue)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_valid_vote_count_result_item.numValue * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.seatsAllocated))

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-NL-1-LETTER.html',
                content=content
            )

            return html

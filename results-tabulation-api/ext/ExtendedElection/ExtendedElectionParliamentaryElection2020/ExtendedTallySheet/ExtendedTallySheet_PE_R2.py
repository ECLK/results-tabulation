from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_SEAT_CALCULATION_CANNOT_BE_DONE_ON_ZERO_VOTES
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.META_DATA_KEY import \
    META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION, \
    META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, \
    TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
from flask import render_template
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum
import math
import pandas as pd
import numpy as np

template_row_to_df_num_value_column_map = {
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: "seatsAllocatedFromRound1",
    TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: "validVotesRemainFromRound1",
    TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: "draftSeatsAllocatedFromRound2",
    TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED: "draftBonusSeatsAllocated",
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: "seatsAllocatedFromRound2",
    TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: "bonusSeatsAllocated",
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: "voteCountCeilPerSeat",
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION: "minimumVoteCountRequiredForSeatAllocation"
}


class ExtendedTallySheet_PE_R2(ExtendedEditableTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):

        def get_post_save_request_content(self):
            election = self.tallySheetVersion.submission.election
            tally_sheet_id = self.tallySheetVersion.tallySheetId

            minimum_vote_count_percentage_required = election.meta.get_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION)
            if minimum_vote_count_percentage_required is not None:
                minimum_vote_count_percentage_required = float(minimum_vote_count_percentage_required)

            number_of_seats_allocated = election.meta.get_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED)
            if number_of_seats_allocated is not None:
                number_of_seats_allocated = int(number_of_seats_allocated)

            df = self.populate_seats_per_party(
                minimum_vote_count_percentage_required=minimum_vote_count_percentage_required,
                number_of_seats_allocated=number_of_seats_allocated
            )

            template_row_map = {
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: [],
                TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: [],
                TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: [],
                TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED: [],
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: [],
                TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: [],
                TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: [],
                TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION: []
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

        def populate_seats_per_party(self, minimum_vote_count_percentage_required, number_of_seats_allocated=0):
            df = self.get_party_wise_valid_vote_count_result()

            total_valid_vote_count = df['numValue'].sum()

            if total_valid_vote_count == 0:
                raise ForbiddenException(
                    message="Seat calculation cannot be done on zero votes.",
                    code=MESSAGE_CODE_SEAT_CALCULATION_CANNOT_BE_DONE_ON_ZERO_VOTES
                )

            _minimum_valid_vote_count_required_per_party_to_be_qualified = total_valid_vote_count * minimum_vote_count_percentage_required

            total_valid_vote_count_of_qualified_parties = 0

            for index in df.index:
                if df.at[index, 'numValue'] >= _minimum_valid_vote_count_required_per_party_to_be_qualified:
                    df.at[index, 'qualifiedForSeatsAllocation'] = True
                    total_valid_vote_count_of_qualified_parties += df.at[index, 'numValue']
                else:
                    df.at[index, 'qualifiedForSeatsAllocation'] = False

            max_valid_vote_count_per_party = df['numValue'].max()

            for index in df.index:
                if df.at[index, 'numValue'] == max_valid_vote_count_per_party:
                    df.at[index, 'bonusSeatsAllocated'] = 1
                    number_of_seats_allocated -= 1
                else:
                    df.at[index, 'bonusSeatsAllocated'] = 0

            valid_vote_count_required_per_seat = total_valid_vote_count_of_qualified_parties / number_of_seats_allocated
            valid_vote_count_required_per_seat_ceil = math.ceil(valid_vote_count_required_per_seat)

            for index in df.index:
                num_value = df.at[index, 'numValue']
                if df.at[index, 'qualifiedForSeatsAllocation']:
                    number_of_seats_qualified = math.floor(num_value / valid_vote_count_required_per_seat_ceil)
                    df.at[index, 'seatsAllocatedFromRound1'] = number_of_seats_qualified
                    number_of_seats_allocated -= number_of_seats_qualified
                    df.at[index, 'validVotesRemainFromRound1'] = num_value % valid_vote_count_required_per_seat_ceil
                else:
                    df.at[index, 'seatsAllocatedFromRound1'] = 0
                    df.at[index, 'validVotesRemainFromRound1'] = 0

            df = df.sort_values(by=['validVotesRemainFromRound1'], ascending=False)
            for index in df.index:
                if df.at[index, 'qualifiedForSeatsAllocation'] and number_of_seats_allocated > 0:
                    number_of_seats_qualified = 1
                    df.at[index, 'seatsAllocatedFromRound2'] = number_of_seats_qualified
                    number_of_seats_allocated -= number_of_seats_qualified
                else:
                    df.at[index, 'seatsAllocatedFromRound2'] = 0

            df['seatsAllocated'] = df.seatsAllocatedFromRound1 + df.seatsAllocatedFromRound2 + df.bonusSeatsAllocated

            df['draftSeatsAllocatedFromRound2'] = df.seatsAllocatedFromRound2
            df['draftBonusSeatsAllocated'] = df.bonusSeatsAllocated

            df = df.sort_values(by=['numValue'], ascending=False)

            df["voteCountCeilPerSeat"] = pd.Series(
                np.full(len(df.index), valid_vote_count_required_per_seat_ceil),
                index=df.index)
            df["minimumVoteCountRequiredForSeatAllocation"] = pd.Series(
                np.full(len(df.index), _minimum_valid_vote_count_required_per_party_to_be_qualified),
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

            party_wise_calculations_df[
                'seatsAllocated'] = party_wise_calculations_df.seatsAllocatedFromRound1 + party_wise_calculations_df.seatsAllocatedFromRound2 + party_wise_calculations_df.bonusSeatsAllocated

            party_wise_calculations_df = party_wise_calculations_df.sort_values(by=['seatsAllocated'], ascending=False)

            return party_wise_calculations_df

        def html(self, title="", total_registered_voters=None):
            party_wise_seat_calculations = self.get_party_wise_seat_calculations()

            totalVoteCounts = to_comma_seperated_num(party_wise_seat_calculations['numValue'].sum())
            twentiethOfTotalVoteCounts = party_wise_seat_calculations.at[0, 'minimumVoteCountRequiredForSeatAllocation']
            total_less_than_twentiethOfTotalVoteCounts = party_wise_seat_calculations[
                party_wise_seat_calculations["numValue"] < twentiethOfTotalVoteCounts
                ]["numValue"].sum()

            total_votes_after_deduction = party_wise_seat_calculations[
                                              'numValue'].sum() - total_less_than_twentiethOfTotalVoteCounts
            number_of_members_to_be_elected_minus_1 = party_wise_seat_calculations['seatsAllocated'].sum() - 1
            relevant_no_of_votes_div_by_no_of_members = total_votes_after_deduction / number_of_members_to_be_elected_minus_1
            rounded_relevant_no_of_votes_div_by_no_of_members = math.ceil(relevant_no_of_votes_div_by_no_of_members)

            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            pollingDivision = tallySheetVersion.submission.area.areaName
            if tallySheetVersion.submission.election.voteType == Postal:
                pollingDivision = 'Postal'

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PE/R2",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "electoralDistrictId": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaId,
                "data": [],
                "rejectedVoteCounts": [],
                "totalVoteCounts": to_comma_seperated_num(totalVoteCounts),
                "twentiethOfTotalVoteCounts": to_comma_seperated_num(twentiethOfTotalVoteCounts, num_type=float),
                "total_less_than_twentiethOfTotalVoteCounts": to_comma_seperated_num(
                    total_less_than_twentiethOfTotalVoteCounts),
                "total_votes_after_deduction": to_comma_seperated_num(total_votes_after_deduction),
                "number_of_members_to_be_elected_minus_1": to_comma_seperated_num(
                    number_of_members_to_be_elected_minus_1),
                "relevant_no_of_votes_div_by_no_of_members": to_comma_seperated_num(
                    relevant_no_of_votes_div_by_no_of_members),
                "rounded_relevant_no_of_votes_div_by_no_of_members": to_comma_seperated_num(
                    rounded_relevant_no_of_votes_div_by_no_of_members),
                "total": []
            }

            total_seatsAllocatedFromRound1 = 0
            total_seatsAllocatedFromRound2 = 0
            total_bonusSeatsAllocated = 0

            party_wise_seat_calculations = party_wise_seat_calculations[
                party_wise_seat_calculations["numValue"] >= twentiethOfTotalVoteCounts
                ]

            for party_wise_seat_calculation_item in party_wise_seat_calculations.itertuples():
                data_row = []

                data_row.append(party_wise_seat_calculation_item.partyName)
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.numValue))
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.seatsAllocatedFromRound1))
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.validVotesRemainFromRound1))
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.seatsAllocatedFromRound2))
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.bonusSeatsAllocated))
                data_row.append(to_comma_seperated_num(party_wise_seat_calculation_item.seatsAllocated))

                content["data"].append(data_row)

                total_seatsAllocatedFromRound1 += int(party_wise_seat_calculation_item.seatsAllocatedFromRound1)
                total_seatsAllocatedFromRound2 += int(party_wise_seat_calculation_item.seatsAllocatedFromRound2)
                total_bonusSeatsAllocated += int(party_wise_seat_calculation_item.bonusSeatsAllocated)

            # get the totals
            content["total"].append(to_comma_seperated_num(total_votes_after_deduction))
            content["total"].append(to_comma_seperated_num(total_seatsAllocatedFromRound1))
            content["total"].append(to_comma_seperated_num(total_seatsAllocatedFromRound2))
            content["total"].append(to_comma_seperated_num(total_bonusSeatsAllocated))
            content["total"].append(to_comma_seperated_num(party_wise_seat_calculations['seatsAllocated'].sum()))

            html = render_template(
                'PE-R2.html',
                content=content
            )

            # return super(ExtendedTallySheet_PE_R2.ExtendedTallySheetVersion, self).html(
            #     title="PE-R2 : %s" % self.tallySheetVersion.submission.area.areaName,
            #     columns=[
            #         "partyId",
            #         "partyName",
            #         "partySymbol",
            #         "partyAbbreviation",
            #         "numValue",
            #         "voteCountCeilPerSeat",
            #         "minimumVoteCountRequiredForSeatAllocation",
            #         "draftBonusSeatsAllocated",
            #         "draftSeatsAllocatedFromRound2",
            #         "bonusSeatsAllocated",
            #         "seatsAllocatedFromRound1",
            #         "validVotesRemainFromRound1",
            #         "seatsAllocatedFromRound2",
            #         "seatsAllocated"
            #     ],
            #     df=party_wise_seat_calculations
            # )

            return html

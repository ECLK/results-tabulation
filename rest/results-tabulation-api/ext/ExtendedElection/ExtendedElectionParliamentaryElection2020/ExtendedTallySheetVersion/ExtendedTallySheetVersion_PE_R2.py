from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_CANNOT_DIVIDE_BY_ZERO
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_QUALIFIED_FOR_SEAT_ALLOCATION
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
import math


class ExtendedTallySheetVersion_PE_R2(ExtendedTallySheetVersion):

    def get_post_save_request_content(self):
        tally_sheet_id = self.tallySheetVersion.tallySheetId

        total_valid_vote_count, total_valid_vote_count_of_qualified_parties, valid_vote_count_required_per_seat, \
        valid_vote_count_required_per_seat_ceil, df = self.get_seats_per_party(
            minimum_vote_count_percentage_required=0.1,
            number_of_seats_allocated=10
        )

        template_row_map = {
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: [],
            TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: [],
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: [],
            TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: [],
            TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: [],
            TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_QUALIFIED_FOR_SEAT_ALLOCATION: []
        }

        template_row_to_df_num_value_column_map = {
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: "seatsAllocatedFromRound1",
            TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: "validVotesRemainFromRound1",
            TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: "seatsAllocatedFromRound2",
            TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: "bonusSeatsAllocated"
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

        for index, row in df.iterrows():
            for templateRowType in template_row_to_df_num_value_column_map.keys():
                for templateRow in template_row_map[templateRowType]:
                    content.append({
                        "templateRowId": templateRow.templateRowId,
                        "templateRowType": templateRowType,
                        "partyId": int(df.at[index, "partyId"]),
                        "numValue": float(df.at[index, template_row_to_df_num_value_column_map[templateRowType]])
                    })

        for templateRow in template_row_map[TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT]:
            content.append({
                "templateRowId": templateRow.templateRowId,
                "templateRowType": TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT,
                "partyId": int(df.at[index, "partyId"]),
                "numValue": valid_vote_count_required_per_seat_ceil
            })

        for templateRow in template_row_map[TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_QUALIFIED_FOR_SEAT_ALLOCATION]:
            content.append({
                "templateRowId": templateRow.templateRowId,
                "templateRowType": TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_QUALIFIED_FOR_SEAT_ALLOCATION,
                "partyId": int(df.at[index, "partyId"]),
                "numValue": total_valid_vote_count_of_qualified_parties
            })

        print("##################################")
        print("template_row_map : ", template_row_map)
        print(df)
        print("##################################")

        return content

    def get_seats_per_party(self, minimum_vote_count_percentage_required, number_of_seats_allocated=0):
        df = self.get_party_wise_valid_vote_count_result()

        total_valid_vote_count = df['numValue'].sum()

        if total_valid_vote_count == 0:
            raise ForbiddenException(
                message="Seat calculation cannot be done on zero votes.",
                code=MESSAGE_CODE_CANNOT_DIVIDE_BY_ZERO
            )

        _minimum_valid_vote_count_required_per_party_to_be_qualified = (
                total_valid_vote_count * minimum_vote_count_percentage_required)

        total_valid_vote_count_of_qualified_parties = 0

        for index, row in df.iterrows():
            if df.at[index, 'numValue'] >= _minimum_valid_vote_count_required_per_party_to_be_qualified:
                df.at[index, 'qualifiedForSeatsAllocation'] = True
                total_valid_vote_count_of_qualified_parties += df.at[index, 'numValue']
            else:
                df.at[index, 'qualifiedForSeatsAllocation'] = False

        max_valid_vote_count_per_party = df['numValue'].max()

        for index, row in df.iterrows():
            if row.numValue == max_valid_vote_count_per_party:
                df.at[index, 'bonusSeatsAllocated'] = 1
                number_of_seats_allocated -= 1
            else:
                df.at[index, 'bonusSeatsAllocated'] = 0

        valid_vote_count_required_per_seat = total_valid_vote_count_of_qualified_parties / number_of_seats_allocated
        valid_vote_count_required_per_seat_ceil = math.ceil(valid_vote_count_required_per_seat)

        for index, row in df.iterrows():
            if df.at[index, 'qualifiedForSeatsAllocation']:
                number_of_seats_qualified = math.floor(row.numValue / valid_vote_count_required_per_seat_ceil)
                df.at[index, 'seatsAllocatedFromRound1'] = number_of_seats_qualified
                number_of_seats_allocated -= number_of_seats_qualified
                df.at[index, 'validVotesRemainFromRound1'] = row.numValue % valid_vote_count_required_per_seat_ceil
            else:
                df.at[index, 'seatsAllocatedFromRound1'] = 0
                df.at[index, 'validVotesRemainFromRound1'] = 0

        df = df.sort_values(by=['validVotesRemainFromRound1'], ascending=False)
        for index, row in df.iterrows():
            if df.at[index, 'qualifiedForSeatsAllocation'] and number_of_seats_allocated > 0:
                number_of_seats_qualified = 1
                df.at[index, 'seatsAllocatedFromRound2'] = number_of_seats_qualified
                number_of_seats_allocated -= number_of_seats_qualified
            else:
                df.at[index, 'seatsAllocatedFromRound2'] = 0

        df['seatsAllocated'] = df.seatsAllocatedFromRound1 + df.seatsAllocatedFromRound2 + df.bonusSeatsAllocated

        df = df.sort_values(by=['numValue'], ascending=False)

        return total_valid_vote_count, total_valid_vote_count_of_qualified_parties, \
               valid_vote_count_required_per_seat, valid_vote_count_required_per_seat_ceil, df

    # def html(self, title="", total_registered_voters=None):
    #     total_valid_vote_count, total_valid_vote_count_of_qualified_parties, valid_vote_count_required_per_seat, \
    #     valid_vote_count_required_per_seat_ceil, df = self.get_seats_per_party(
    #         minimum_vote_count_percentage_required=0.1,
    #         number_of_seats_allocated=10
    #     )
    #
    #     print(df)
    #
    #     return super(ExtendedTallySheetVersion_PE_R2, self).html(
    #         title="PE-R2 : %s" % self.tallySheetVersion.submission.area.areaName,
    #         columns=[
    #             "tallySheetVersionRowId",
    #             "electionId",
    #             "partyId",
    #             "partyName",
    #             "partySymbol",
    #             "partyAbbreviation",
    #             "numValue",
    #             "qualifiedForSeatsAllocation",
    #             "bonusSeatsAllocated",
    #             "seatsAllocatedFromRound1",
    #             "validVotesRemainFromRound1",
    #             "seatsAllocatedFromRound2",
    #             "seatsAllocated"
    #         ],
    #         df=df
    #     )

    # TODO

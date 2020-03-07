from app import db
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
import math


class ExtendedTallySheetVersion_PE_21(ExtendedTallySheetVersion):

    def get_post_save_request_content(self):
        tally_sheet_id = self.tallySheetVersion.tallySheetId
        template_rows = db.session.query(
            TemplateRowModel.templateRowId
        ).filter(
            TemplateModel.templateId == TallySheet.Model.templateId,
            TemplateRowModel.templateId == TemplateModel.templateId,
            TemplateRowModel.templateRowType == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
            TallySheet.Model.tallySheetId == tally_sheet_id
        ).group_by(
            TemplateRowModel.templateRowId
        ).all()

        content = []

        candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result().sort_values(
            by=['numValue'], ascending=False
        )
        seats_allocated_per_party_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED]
        for index_1 in seats_allocated_per_party_df.index:
            party_id = seats_allocated_per_party_df.at[index_1, "partyId"]
            number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]

            if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):
                filtered_candidate_wise_valid_vote_count_result = candidate_wise_valid_vote_count_result.loc[
                    candidate_wise_valid_vote_count_result["partyId"] == party_id]
                for index_2 in filtered_candidate_wise_valid_vote_count_result.index:
                    if number_of_seats_allocated > 0:
                        for template_row in template_rows:
                            content.append({
                                "templateRowId": template_row.templateRowId,
                                "templateRowType": TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
                                "partyId": int(party_id),
                                "candidateId": int(
                                    filtered_candidate_wise_valid_vote_count_result.at[index_2, "candidateId"]),
                                "numValue": int(
                                    filtered_candidate_wise_valid_vote_count_result.at[index_2, "numValue"])
                            })
                        number_of_seats_allocated -= 1

        return content

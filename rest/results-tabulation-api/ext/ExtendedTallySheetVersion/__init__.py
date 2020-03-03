import pandas as pd
from flask import render_template
from constants.VOTE_TYPES import Postal, NonPostal
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri


def get_extended_tally_sheet_version_class(templateName):
    EXTENDED_TEMPLATE_MAP = {
        # TODO
    }

    if templateName in EXTENDED_TEMPLATE_MAP:
        return EXTENDED_TEMPLATE_MAP[templateName]
    else:
        return ExtendedTallySheetVersion


class ExtendedTallySheetVersion:
    def __init__(self, tallySheetVersion):
        self.tallySheetVersion = tallySheetVersion

        data = tallySheetVersion.content
        self.df = pd.DataFrame(data)

    def html_letter(self, title="", total_registered_voters=None):
        tallySheetVersion = self.tallySheetVersion
        stamp = tallySheetVersion.stamp

        if total_registered_voters is None:
            total_registered_voters = float(tallySheetVersion.submission.area.registeredVotersCount)

        content = {
            "resultTitle": title,
            "election": {
                "electionName": tallySheetVersion.submission.election.get_official_name()
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
                to_comma_seperated_num(total_registered_voters),
                100
            ]
        }

        candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
        vote_count_result = self.get_vote_count_result()
        valid_vote_count_result = self.get_valid_vote_count_result()
        rejected_vote_count_result = self.get_rejected_vote_count_result()

        for candidate_wise_valid_non_postal_vote_count_result_item in candidate_wise_valid_vote_count_result.itertuples():
            content["data"].append([
                candidate_wise_valid_non_postal_vote_count_result_item.candidateName,
                candidate_wise_valid_non_postal_vote_count_result_item.partyAbbreviation,
                to_comma_seperated_num(candidate_wise_valid_non_postal_vote_count_result_item.numValue),
                to_percentage(candidate_wise_valid_non_postal_vote_count_result_item.numValue * 100 /
                              valid_vote_count_result["numValue"].values[0]) if
                valid_vote_count_result["numValue"].values[
                    0] > 0 else ""
            ])

        content["validVoteCounts"] = [
            to_comma_seperated_num(valid_vote_count_result["numValue"].values[0]),
            to_percentage(valid_vote_count_result["numValue"].values[0] * 100 / vote_count_result["numValue"].values[0])
            if vote_count_result["numValue"].values[0] > 0 else ""
        ]

        content["rejectedVoteCounts"] = [
            to_comma_seperated_num(rejected_vote_count_result["numValue"].values[0]),
            rejected_vote_count_result["numValue"].values[0] * 100 / vote_count_result["numValue"].values[0]
            if vote_count_result["numValue"].values[0] > 0 else ""
        ]

        content["totalVoteCounts"] = [
            to_comma_seperated_num(vote_count_result["numValue"].values[0]),
            to_percentage(vote_count_result["numValue"].values[0] * 100 / total_registered_voters)
        ]

        content["logo"] = convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png")

        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=content
        )

        return html

    def html(self, title="", total_registered_voters=None):
        stamp = self.tallySheetVersion.stamp

        content = {
            "columns": [
                "tallySheetVersionRowId",
                "electionId",
                "templateRowId",
                "templateRowType",
                "electionId",
                "voteType",
                "rootElectionId",
                "areaId",
                "areaName",
                "candidateId",
                "candidateName",
                "partyId",
                "partyName",
                "partySymbol",
                "partyAbbreviation",
                "invalidVoteCategoryId",
                "invalidVoteCategoryDescription",
                "strValue",
                "numValue"
            ],
            "data": [],
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
        }

        for row in self.tallySheetVersion.content:
            content_row = [
                row.tallySheetVersionRowId,
                row.electionId,
                row.templateRowId,
                row.templateRowType,
                row.electionId,
                row.voteType,
                row.rootElectionId,
                row.areaId,
                row.areaName,
                row.candidateId,
                row.candidateName,
                row.partyId,
                row.partyName,
                row.partySymbol,
                row.partyAbbreviation,
                row.invalidVoteCategoryId,
                row.invalidVoteCategoryDescription,
                row.strValue,
                row.numValue
            ]

            content_row = ["" if cell is None else cell for cell in content_row]

            content["data"].append(content_row)

        html = render_template(
            'DEFAULT.html',
            content=content
        )

        return html

    def get_candidate_and_area_wise_valid_non_postal_vote_count_result(self):
        df = self.df.copy()

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.sort_values(
            by=['partyId', 'candidateId', 'areaId'], ascending=True
        ).reset_index()

        return df

    def get_party_and_area_wise_valid_non_postal_vote_count_result(self):
        df = self.df.copy()

        df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.sort_values(
            by=['partyId', 'areaId'], ascending=True
        ).reset_index()

        return df

    def get_candidate_wise_valid_non_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(
            ['partyId', 'partyName', 'partyAbbreviation', 'candidateId', 'candidateName']
        ).agg(sum).sort_values(
            by=['partyId', 'candidateId'], ascending=True
        ).reset_index()

        return df

    def get_candidate_wise_valid_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(
            ['partyId', 'partyName', 'partyAbbreviation', 'candidateId', 'candidateName']
        ).agg(sum).sort_values(
            by=['partyId', 'candidateId'], ascending=True
        ).reset_index()

        return df

    def get_party_wise_valid_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(
            ['partyId', 'partyName', 'partyAbbreviation']
        ).agg({'numValue': lambda x: x.sum(skipna=False)}).sort_values(
            by=['partyId'], ascending=True
        ).reset_index()

        return df

    def get_candidate_wise_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

        df = df.groupby(
            ['partyId', 'partyName', 'partyAbbreviation', 'candidateId', 'candidateName']
        ).agg(sum).sort_values(
            by=['partyId', 'candidateId'], ascending=True
        ).reset_index()

        return df

    def get_area_wise_valid_non_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[(df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_area_wise_rejected_non_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_area_wise_non_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_non_postal_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_non_postal_rejected_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_non_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)
        df = df.loc[df['voteType'] == NonPostal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_postal_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_party_wise_postal_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_postal_rejected_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_postal_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)
        df = df.loc[df['voteType'] == Postal]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[(df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_rejected_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.groupby(lambda a: True).agg(sum)

        return df

    def get_candidate_and_area_wise_valid_vote_count_result(self):
        df = self.df.copy()

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

        df = df.sort_values(
            by=['partyId', 'candidateId', 'areaId'], ascending=True
        ).reset_index()

        return df


    def get_party_and_area_wise_valid_vote_count_result(self):
        df = self.df.copy()

        df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

        df = df.sort_values(
            by=['partyId', 'areaId'], ascending=True
        ).reset_index()
        return df

    def get_area_wise_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[(df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_party_wise_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

        df = df.groupby(
            ['partyId', 'partyName', 'partyAbbreviation']
        ).agg(sum).sort_values(
            by=['partyId'], ascending=True
        ).reset_index()

        return df

    def get_area_wise_rejected_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_area_wise_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    def get_polling_station_wise_number_of_ballots_recieved(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)
        df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_RECEIVED"]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

    # def get_polling_station_wise_number_of_spoilt_ballot_papers(self):
    #     df = self.df.copy()
    #     df['numValue'] = df['numValue'].astype(float)
    #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_SPOILT"]
    #
    #     df = df.groupby(
    #         ['areaId', "areaName"]
    #     ).agg(sum).sort_values(
    #         by=['areaId'], ascending=True
    #     ).reset_index()
    #
    #     return df
    #
    # def get_polling_station_wise_number_of_issued_ballot_papers(self):
    #     df = self.df.copy()
    #     df['numValue'] = df['numValue'].astype(float)
    #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_ISSUED"]
    #
    #     df = df.groupby(
    #         ['areaId', "areaName"]
    #     ).agg(sum).sort_values(
    #         by=['areaId'], ascending=True
    #     ).reset_index()
    #
    #     return df
    #
    # def get_polling_station_wise_number_of_unused_ballot_papers(self):
    #     df = self.df.copy()
    #     df['numValue'] = df['numValue'].astype(float)
    #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_UNUSED"]
    #
    #     df = df.groupby(
    #         ['areaId', "areaName"]
    #     ).agg(sum).sort_values(
    #         by=['areaId'], ascending=True
    #     ).reset_index()
    #
    #     return df
    # 
    # def get_polling_station_wise_number_of_ordinary_ballots_in_ballot_paper_account(self):
    #     df = self.df.copy()
    #     df['numValue'] = df['numValue'].astype(float)
    #     df = df.loc[df['templateRowType'] == "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT"]
    #
    #     df = df.groupby(
    #         ['areaId', "areaName"]
    #     ).agg(sum).sort_values(
    #         by=['areaId'], ascending=True
    #     ).reset_index()
    #
    #     return df

    def get_polling_station_wise_number_of_ordinary_ballots_in_ballot_box(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)
        df = df.loc[df['templateRowType'] == "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX"]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
        ).reset_index()

        return df

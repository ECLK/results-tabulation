import pandas as pd
from flask import render_template
from constants.VOTE_TYPES import Postal, NonPostal
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri


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
            "resultTitle": "All Island Result",
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
        return self.html_letter(title=title, total_registered_voters=total_registered_voters)

    def get_candidate_and_area_wise_valid_non_postal_vote_count_result(self):
        df = self.df.copy()

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
        df = df.loc[df['voteType'] == NonPostal]

        df = df.sort_values(
            by=['partyId', 'candidateId', 'areaId'], ascending=True
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

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
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

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

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

    def get_area_wise_valid_vote_count_result(self):
        df = self.df.copy()
        df['numValue'] = df['numValue'].astype(float)

        df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

        df = df.groupby(
            ['areaId', "areaName"]
        ).agg(sum).sort_values(
            by=['areaId'], ascending=True
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

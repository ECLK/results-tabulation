from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheet
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_CE_201(ExtendedTallySheet):
    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_CE_201.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
            )

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            polling_station_wise_number_of_ballots_recieved = self.get_polling_station_wise_number_of_ballots_recieved()
            # polling_station_wise_number_of_spoilt_ballot_papers = self.get_polling_station_wise_number_of_spoilt_ballot_papers()
            # polling_station_wise_number_of_issued_ballot_papers = self.get_polling_station_wise_number_of_issued_ballot_papers()
            # polling_station_wise_number_of_unused_ballot_papers = self.get_polling_station_wise_number_of_unused_ballot_papers()
            # polling_station_wise_number_of_ordinary_ballots_in_ballot_paper_account = self.get_polling_station_wise_number_of_ordinary_ballots_in_ballot_paper_account()
            polling_station_wise_number_of_ordinary_ballots_in_ballot_box = self.get_polling_station_wise_number_of_ordinary_ballots_in_ballot_box()

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
                "tallySheetCode": "CE-201",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "parliamentaryElection": 1,
                "data": []
            }

            # Appending polling station wise ballot counts

            for polling_station_wise_number_of_ballots_recieved_item_index, polling_station_wise_number_of_ballots_recieved_item in polling_station_wise_number_of_ballots_recieved.iterrows():
                data_row = []

                data_row.append(Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.PollingDistrict)[
                                    polling_station_wise_number_of_ballots_recieved_item_index].areaName)
                data_row.append(polling_station_wise_number_of_ballots_recieved_item.areaName)
                # data_row.append(to_comma_seperated_num(polling_station_wise_number_of_ballots_recieved_item.numValue))

                # data_row.append(to_comma_seperated_num(polling_station_wise_number_of_spoilt_ballot_papers["numValue"].values[
                #             polling_station_wise_number_of_ballots_recieved_item_index]))
                # data_row.append(to_comma_seperated_num(polling_station_wise_number_of_issued_ballot_papers["numValue"].values[
                #             polling_station_wise_number_of_ballots_recieved_item_index]))
                # data_row.append(to_comma_seperated_num(polling_station_wise_number_of_unused_ballot_papers["numValue"].values[
                #             polling_station_wise_number_of_ballots_recieved_item_index]))
                # data_row.append(to_comma_seperated_num(polling_station_wise_number_of_ordinary_ballots_in_ballot_paper_account["numValue"].values[
                #             polling_station_wise_number_of_ballots_recieved_item_index]))
                data_row.append(
                    to_comma_seperated_num(
                        polling_station_wise_number_of_ordinary_ballots_in_ballot_box["numValue"].values[
                            polling_station_wise_number_of_ballots_recieved_item_index]))

                content["data"].append(data_row)

            html = render_template(
                'CE-201.html',
                content=content
            )

            return html

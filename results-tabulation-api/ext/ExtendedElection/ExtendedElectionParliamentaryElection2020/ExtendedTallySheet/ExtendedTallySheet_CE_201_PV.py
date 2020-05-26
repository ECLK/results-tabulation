from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheetDataEntry
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_CE_201_PV(ExtendedTallySheetDataEntry):
    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_CE_201_PV.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
            )

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion


            time_of_commencement = self.get_time_of_commencement()
            number_of_a_packets_found = self.get_number_of_a_packets_found()
            ballot_box_serial_number = self.get_ballot_box_serial_number()
            no_of_packets_inserted_to_ballot_box = self.get_no_of_packets_inserted_to_ballot_box()
            number_of_a_covers_rejected = self.get_number_of_a_covers_rejected()
            number_of_b_covers_rejected = self.get_number_of_b_covers_rejected()

            accepted_ballots = number_of_a_packets_found['numValue'].sum() - (number_of_a_covers_rejected['numValue'].values[0] +
                number_of_b_covers_rejected['numValue'].values[0])

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
                "tallySheetCode": "CE-201-PV",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "timeOfCommencementOfCount": time_of_commencement["strValue"].values[0],
                "numberOfAPacketsFound": to_comma_seperated_num(number_of_a_packets_found['numValue'].sum()),
                "numberOfACoversRejected": number_of_a_covers_rejected['numValue'].values[0],
                "numberOfBCoversRejected": number_of_b_covers_rejected['numValue'].values[0],
                "numberOfValidBallotPapers": accepted_ballots,
                "parliamentaryElection": 1,
                "data": []
            }

            # Appending polling station wise ballot counts
            index = 0

            for ballot_box_serial_number_item_index, ballot_box_serial_number_item in ballot_box_serial_number.iterrows():
                data_row = []

                data_row.append(ballot_box_serial_number_item.strValue)
                data_row.append(no_of_packets_inserted_to_ballot_box["numValue"].values[index])
                data_row.append(number_of_a_packets_found["numValue"].values[index])
                index += 1

                content["data"].append(data_row)

            html = render_template(
                'CE-201-PV.html',
                content=content
            )

            return html

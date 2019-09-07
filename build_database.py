import csv
import os

from app import db
from orm.entities import *
from orm.entities import Invoice
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionCE201
from orm.enums import TallySheetCodeEnum, BallotTypeEnum
from util import get_tally_sheet_code

election = Election.create(electionName="Test Election")

data_stores = {}

csv_dir = ''


def get_data_store(data_store_key):
    if data_store_key not in data_stores:
        data_stores[data_store_key] = {}

    return data_stores[data_store_key]


def get_object_from_data_store(data_key, data_store_key):
    data_store = get_data_store(data_store_key)
    if data_key in data_store:
        return data_store[data_key]
    else:
        return None


def set_object_to_data_store(data_key, data_store_key, obj):
    data_store = get_data_store(data_store_key)
    data_store[data_key] = obj


def get_object(row, row_key, data_key=None):
    if data_key is None:
        cell = row[row_key].strip()
        data_key = cell
    else:
        cell = row[data_key].strip()
        data_key = cell

    data_store_key = row_key

    if data_store_key == "TallySheet":
        data_key = "%s-%s" % (row["TallySheet"], row["Counting Centre"])
    elif data_store_key == "Polling District":
        data_key = "%s-%s" % (row["Polling Division"], row["Polling District"])

    obj = get_object_from_data_store(data_key, data_store_key)

    if obj is None:
        if data_store_key == "Ballot":
            obj = Ballot.create(ballotId=cell, electionId=election.electionId)
        elif data_store_key == "Tendered Ballot":
            obj = Ballot.create(ballotId=cell, electionId=election.electionId, ballotType=BallotTypeEnum.Tendered)
        elif data_store_key == "Ballot Box":
            obj = BallotBox.create(ballotBoxId=cell, electionId=election.electionId)

        elif data_store_key == "Party":
            obj = Party.create(partyName=cell, partySymbol=row["Party Symbol"])
        elif data_store_key == "Candidate":
            obj = Candidate.create(candidateName=cell)

        elif data_store_key == "Country":
            obj = Country.create(cell, electionId=election.electionId)


        elif data_store_key == "Electoral District":
            obj = ElectoralDistrict.create(cell, electionId=election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_30_ED, electionId=election.electionId, officeId=obj.areaId
            )


        elif data_store_key == "Polling Division":
            obj = PollingDivision.create(cell, electionId=election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_30_PD, electionId=election.electionId, officeId=obj.areaId
            )


        elif data_store_key == "Polling District":
            obj = PollingDistrict.create(cell, electionId=election.electionId)

        elif data_store_key == "Election Commission":
            obj = ElectionCommission.create(cell, electionId=election.electionId)
        elif data_store_key == "District Centre":
            obj = DistrictCentre.create(cell, electionId=election.electionId)
        elif data_store_key == "Counting Centre":
            obj = CountingCentre.create(cell, electionId=election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_41, electionId=election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_21, electionId=election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.CE_201, electionId=election.electionId, officeId=obj.areaId
            )


        elif data_store_key == "Polling Station":
            obj = PollingStation.create(cell, electionId=election.electionId)

        elif data_store_key == "TallySheet":
            countingCentre = get_object(row, "Counting Centre")
            tallySheetCode = get_tally_sheet_code(cell)

            obj = TallySheet.create(
                tallySheetCode=tallySheetCode,
                electionId=election.electionId,
                officeId=countingCentre.areaId
            )

            if len(countingCentre.districtCentres) > 0:
                districtCentres = countingCentre.districtCentres[0]

                if tallySheetCode is TallySheetCodeEnum.PRE_41:
                    sampleTallySheetDataRows = get_rows_from_csv('tallysheets/%s/%s/PRE-41.csv' % (
                        districtCentres.areaName, countingCentre.areaName)
                                                                 )

                    if len(sampleTallySheetDataRows) > 0:
                        tallySheetVersion = TallySheetVersionPRE41.create(tallySheetId=obj.tallySheetId)

                        for sampleTallySheetDataRow in sampleTallySheetDataRows:
                            candidate = get_object(sampleTallySheetDataRow, "Candidate")
                            tallySheetVersion.add_row(
                                candidateId=candidate.candidateId,
                                count=sampleTallySheetDataRow["Count"],
                                countInWords=sampleTallySheetDataRow["Count in words"]
                            )
                elif tallySheetCode is TallySheetCodeEnum.CE_201:
                    sampleTallySheetDataRows = get_rows_from_csv(
                        'tallysheets/%s/%s/CE-201.csv' % (
                            districtCentres.areaName, countingCentre.areaName)
                    )

                    if len(sampleTallySheetDataRows) > 0:
                        tallySheetVersion = TallySheetVersionCE201.create(tallySheetId=obj.tallySheetId)

                        for sampleTallySheetDataRow in sampleTallySheetDataRows:
                            pollingStation = get_object(sampleTallySheetDataRow, "Polling Station")
                            tallySheetVersionRow = tallySheetVersion.add_row(
                                areaId=pollingStation.areaId,
                                ballotsIssued=sampleTallySheetDataRow["Issued Ballots"],
                                ballotsReceived=sampleTallySheetDataRow["Received Ballots"],
                                ballotsSpoilt=sampleTallySheetDataRow["Spoilt Ballots"],
                                ballotsUnused=sampleTallySheetDataRow["Unused Ballots"],
                                boxCountOrdinary=sampleTallySheetDataRow["Box Count - Ordinary Ballots"],
                                boxCountTendered=sampleTallySheetDataRow["Box Count - Tendered Ballots"],
                                ballotPaperAccountOrdinary=sampleTallySheetDataRow[
                                    "Ballot Paper Account - Ordinary Ballots"],
                                ballotPaperAccountTendered=sampleTallySheetDataRow[
                                    "Ballot Paper Account - Tendered Ballots"],
                            )

                            receivedBoxIds = sampleTallySheetDataRow["Received Boxes"].split(",")

                            print("####### receivedBoxIds ### ", receivedBoxIds)

                            for receivedBoxId in receivedBoxIds:
                                receivedBox = get_object({"Ballot Box": receivedBoxId}, "Ballot Box")
                                tallySheetVersionRow.add_received_ballot_box(receivedBox.stationaryItemId)


        else:
            print("-------------  Not supported yet : *%s*" % data_store_key)

        set_object_to_data_store(data_key, data_store_key, obj)

    return obj


def get_rows_from_csv(csv_path):
    csv_file_path = "%s/%s" % (csv_dir, csv_path)
    if os.path.exists(csv_file_path) is True:
        with open(csv_file_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            rows = list(reader)
    else:
        rows = []

    return rows


def build_database(dataset):
    global csv_dir

    basedir = os.path.abspath(os.path.dirname(__file__))
    sample_data_dir = os.path.join(basedir, 'sample-data')
    csv_dir = "%s/%s" % (sample_data_dir, dataset)

    for row in get_rows_from_csv('data.csv'):
        print("[ROW] ========= ", row)
        country = get_object({"Country": "Sri Lanka"}, "Country")
        electoralDistrict = get_object(row, "Electoral District")
        pollingDivision = get_object(row, "Polling Division")
        pollingDistrict = get_object(row, "Polling District")
        electionCommission = get_object({"Election Commission": "Sri Lanka Election Commission"}, "Election Commission")
        districtCentre = get_object(row, "District Centre")
        countingCentre = get_object(row, "Counting Centre")
        pollingStation = get_object({"Polling Station": row["Polling Station (English)"]}, "Polling Station")

        country.add_child(electoralDistrict.areaId)
        electoralDistrict.add_child(pollingDivision.areaId)
        pollingDivision.add_child(pollingDistrict.areaId)
        pollingDistrict.add_child(pollingStation.areaId)
        electionCommission.add_child(districtCentre.areaId)
        districtCentre.add_child(countingCentre.areaId)
        countingCentre.add_child(pollingStation.areaId)

        stationaryItems = []

        for i in range(1, 4):
            box_key = "Ballot Box %d" % i
            if box_key in row and row[box_key] is not None and len(row[box_key]) > 0:
                ballotBox = BallotBox.Model(ballotBoxId=row[box_key], electionId=election.electionId)
                db.session.add(ballotBox)
                stationaryItems.append(ballotBox)
                # ballotBox = get_object({"Ballot Box": row[box_key]}, "Ballot Box")

        for ballotId in range(int(row["Ballot - start"]), int(row["Ballot - end"]) + 1):
            ballot = Ballot.Model(ballotId=ballotId, electionId=election.electionId)
            db.session.add(ballot)
            stationaryItems.append(ballot)
            # ballot = get_object({"Ballot": str(ballotId)}, "Ballot")
            # invoice.add_stationary_item(ballot.stationaryItemId)

        for ballotId in range(int(row["Tendered Ballot - start"]), int(row["Tendered Ballot - end"]) + 1):
            ballot = Ballot.Model(ballotId=ballotId, ballotType=BallotTypeEnum.Tendered, electionId=election.electionId)
            db.session.add(ballot)
            stationaryItems.append(ballot)
            # ballot = get_object({"Tendered Ballot": str(ballotId)}, "Tendered Ballot")
            # invoice.add_stationary_item(ballot.stationaryItemId)

        invoice = Invoice.create(
            electionId=election.electionId,
            issuingOfficeId=countingCentre.areaId,
            receivingOfficeId=pollingStation.areaId,
            issuedTo=1
        )

        invoice.add_stationary_items([stationaryItem.stationaryItemId for stationaryItem in stationaryItems])

        invoice.set_confirmed()

        print("[ROW END] ========= ")
    for row in get_rows_from_csv('party-candidate.csv'):
        party = get_object(row, "Party")
        election.add_party(partyId=party.partyId)

        candidate = get_object(row, "Candidate")
        election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)
    for row in get_rows_from_csv('invalid-vote-categories.csv'):
        election.add_invalid_vote_category(row["Invalid Vote Category Description"])
    db.session.commit()

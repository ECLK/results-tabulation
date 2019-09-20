import csv
import os

from app import db
from orm.entities import *
from orm.entities import Invoice
from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, BallotTypeEnum, VoteTypeEnum

root_election = Election.create(electionName="Presidential Election 2019", voteType=VoteTypeEnum.PostalAndNonPostal)

postal_election = root_election.add_sub_election(electionName="Postal", voteType=VoteTypeEnum.Postal)
ordinary_election = root_election.add_sub_election(electionName="Ordinary", voteType=VoteTypeEnum.NonPostal)

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


def get_object(election, row, row_key, data_key=None):
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

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
                electionId=election.electionId,
                officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS,
                electionId=election.electionId,
                officeId=obj.areaId
            )


        elif data_store_key == "Electoral District":
            obj = ElectoralDistrict.create(cell, electionId=election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_30_ED, electionId=election.electionId, officeId=obj.areaId
            )


        elif data_store_key == "Polling Division":
            obj = PollingDivision.create(cell, electionId=election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_30_PD, electionId=ordinary_election.electionId,
                officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_30_PD, electionId=postal_election.electionId,
                officeId=obj.areaId
            )


        elif data_store_key == "Polling District":
            obj = PollingDistrict.create(cell, electionId=election.electionId)

        elif data_store_key == "Election Commission":
            obj = ElectionCommission.create(cell, electionId=election.electionId)
        elif data_store_key == "District Centre":
            obj = DistrictCentre.create(cell, electionId=election.electionId)
        elif data_store_key == "Counting Centre":
            obj = CountingCentre.create(cell, electionId=ordinary_election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_41, electionId=ordinary_election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_21, electionId=ordinary_election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.CE_201, electionId=ordinary_election.electionId, officeId=obj.areaId
            )
        elif data_store_key == "Postal Vote Counting Centre":
            obj = CountingCentre.create(cell, electionId=postal_election.electionId)

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_41, electionId=postal_election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.PRE_21, electionId=postal_election.electionId, officeId=obj.areaId
            )

            TallySheet.create(
                tallySheetCode=TallySheetCodeEnum.CE_201_PV, electionId=postal_election.electionId, officeId=obj.areaId
            )

        elif data_store_key == "Polling Station":
            obj = PollingStation.create(
                cell, electionId=election.electionId,
                registeredVotersCount=row["Registered Voters"]
            )

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
        country = get_object(root_election, {"Country": "Sri Lanka"}, "Country")
        electoralDistrict = get_object(root_election, row, "Electoral District")
        pollingDivision = get_object(root_election, row, "Polling Division")
        pollingDistrict = get_object(root_election, row, "Polling District")
        electionCommission = get_object(root_election, {"Election Commission": "Sri Lanka Election Commission"},
                                        "Election Commission")
        districtCentre = get_object(root_election, row, "District Centre")
        countingCentre = get_object(ordinary_election, row, "Counting Centre")

        pollingStation = get_object(ordinary_election, {
            "Polling Station": row["Polling Station (English)"],
            "Registered Voters": row["Registered Voters"].replace(",", "")
        }, "Polling Station")

        country.add_child(electoralDistrict.areaId)
        electoralDistrict.add_child(pollingDivision.areaId)
        pollingDivision.add_child(pollingDistrict.areaId)
        pollingDistrict.add_child(pollingStation.areaId)
        electionCommission.add_child(districtCentre.areaId)
        districtCentre.add_child(countingCentre.areaId)
        countingCentre.add_child(pollingStation.areaId)

        postalVoteCountingCentre = get_object(postal_election, {
            "Postal Vote Counting Centre": row["Counting Centre"]
        }, "Postal Vote Counting Centre")
        pollingDivision.add_child(postalVoteCountingCentre.areaId)
        districtCentre.add_child(postalVoteCountingCentre.areaId)

        stationaryItems = []

        for i in range(1, 4):
            box_key = "Ballot Box %d" % i
            if box_key in row and row[box_key] is not None and len(row[box_key]) > 0:
                ballotBox = BallotBox.Model(ballotBoxId=row[box_key], electionId=root_election.electionId)
                db.session.add(ballotBox)
                stationaryItems.append(ballotBox)
                # ballotBox = get_object({"Ballot Box": row[box_key]}, "Ballot Box")

        for ballotId in range(int(row["Ballot - start"]), int(row["Ballot - end"]) + 1):
            ballot = Ballot.Model(ballotId=ballotId, electionId=root_election.electionId)
            db.session.add(ballot)
            stationaryItems.append(ballot)
            # ballot = get_object({"Ballot": str(ballotId)}, "Ballot")
            # invoice.add_stationary_item(ballot.stationaryItemId)

        for ballotId in range(int(row["Tendered Ballot - start"]), int(row["Tendered Ballot - end"]) + 1):
            ballot = Ballot.Model(ballotId=ballotId, ballotType=BallotTypeEnum.Tendered,
                                  electionId=root_election.electionId)
            db.session.add(ballot)
            stationaryItems.append(ballot)
            # ballot = get_object({"Tendered Ballot": str(ballotId)}, "Tendered Ballot")
            # invoice.add_stationary_item(ballot.stationaryItemId)

        invoice = Invoice.create(
            electionId=root_election.electionId,
            issuingOfficeId=countingCentre.areaId,
            receivingOfficeId=pollingStation.areaId,
            issuedTo=1
        )

        invoice.add_stationary_items([stationaryItem.stationaryItemId for stationaryItem in stationaryItems])

        invoice.set_confirmed()

        print("[ROW END] ========= ")

    for row in get_rows_from_csv('party-candidate.csv'):
        party = get_object(root_election, row, "Party")
        root_election.add_party(partyId=party.partyId)

        candidate = get_object(root_election, row, "Candidate")
        root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

    for row in get_rows_from_csv('invalid-vote-categories.csv'):
        root_election.add_invalid_vote_category(row["Invalid Vote Category Description"])

    db.session.commit()

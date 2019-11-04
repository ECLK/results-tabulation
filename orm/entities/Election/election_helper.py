import csv
import os

from app import db
from auth import AREA_CLAIM_PREFIX, ADMIN_ROLE, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, \
    EC_LEADERSHIP_ROLE, SUB, ROLE_CLAIM, ROLE_PREFIX
from auth.AuthConstants import NAMESPACE
from orm.entities import *
from orm.entities import Invoice, Area, Election
from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, BallotTypeEnum, VoteTypeEnum, AreaTypeEnum
from jose import jwt


def get_root_token(electionId):
    electoral_districts = Area.Model.query.filter(
        Area.Model.areaType == AreaTypeEnum.ElectoralDistrict,
        Area.Model.electionId == electionId
    ).all()
    countries = Area.Model.query.filter(
        Area.Model.areaType == AreaTypeEnum.Country,
        Area.Model.electionId == electionId
    ).all()

    jwt_payload = {
        ROLE_CLAIM: [
            ROLE_PREFIX + DATA_EDITOR_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + EC_LEADERSHIP_ROLE
        ],
        SUB: "janak@carbon.super", AREA_CLAIM_PREFIX + ADMIN_ROLE: str([]),
        AREA_CLAIM_PREFIX + DATA_EDITOR_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries]),
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries]),
        AREA_CLAIM_PREFIX + EC_LEADERSHIP_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries])
    }

    # Generate a token with claims for everything.
    key = "jwt_secret"
    encoded_jwt_token = jwt.encode(jwt_payload, key)

    return encoded_jwt_token


def build_presidential_election(root_election: Election, party_candidate_dataset_file=None,
                                polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                                invalid_vote_categories_dataset_file=None):
    postal_election = root_election.add_sub_election(electionName="Postal", voteType=VoteTypeEnum.Postal)
    ordinary_election = root_election.add_sub_election(electionName="Ordinary", voteType=VoteTypeEnum.NonPostal)

    if not party_candidate_dataset_file:
        party_candidate_dataset_file = root_election.partyCandidateDataset.get_file_path()

    if not polling_station_dataset_file:
        polling_station_dataset_file = root_election.pollingStationsDataset.get_file_path()

    if not postal_counting_centers_dataset_file:
        postal_counting_centers_dataset_file = root_election.postalCountingCentresDataset.get_file_path()

    if not invalid_vote_categories_dataset_file:
        invalid_vote_categories_dataset_file = root_election.invalidVoteCategoriesDataset.get_file_path()

    data_stores = {}

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
            data_key = "%s-%s-%s" % (row["Electoral District"], row["Polling Division"], row["Polling District"])
        elif data_store_key == "Counting Centre":
            data_key = "%s-%s" % (row["Electoral District"], row["Counting Centre"])

        obj = get_object_from_data_store(data_key, data_store_key)

        if obj is None:
            if data_store_key == "Ballot":
                obj = Ballot.create(ballotId=cell, electionId=election.electionId)
            elif data_store_key == "Tendered Ballot":
                obj = Ballot.create(ballotId=cell, electionId=election.electionId, ballotType=BallotTypeEnum.Tendered)
            elif data_store_key == "Ballot Box":
                obj = BallotBox.create(ballotBoxId=cell, electionId=election.electionId)

            elif data_store_key == "Party":
                obj = Party.create(partyName=cell, partySymbol=row["Party Symbol"],
                                   partyAbbreviation=row["Party Abbreviation"])
            elif data_store_key == "Candidate":
                obj = Candidate.create(candidateName=cell)

            elif data_store_key == "Country":
                obj = Country.create(cell, electionId=election.electionId)

                TallySheet.create(
                    tallySheetCode=TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
                    electionId=election.electionId,
                    areaId=obj.areaId
                )

                TallySheet.create(
                    tallySheetCode=TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS,
                    electionId=election.electionId,
                    areaId=obj.areaId
                )

            elif data_store_key == "Electoral District":
                obj = ElectoralDistrict.create(cell, electionId=election.electionId)

                TallySheet.create(
                    tallySheetCode=TallySheetCodeEnum.PRE_30_ED, electionId=election.electionId, areaId=obj.areaId
                )

                TallySheet.create(
                    tallySheetCode=TallySheetCodeEnum.PRE_30_PD, electionId=postal_election.electionId,
                    areaId=obj.areaId
                )

            elif data_store_key == "Polling Division":
                obj = PollingDivision.create(cell, electionId=election.electionId)

                TallySheet.create(
                    tallySheetCode=TallySheetCodeEnum.PRE_30_PD, electionId=ordinary_election.electionId,
                    areaId=obj.areaId
                )

            elif data_store_key == "Polling District":
                obj = PollingDistrict.create(cell, electionId=election.electionId)

            elif data_store_key == "Election Commission":
                obj = ElectionCommission.create(cell, electionId=election.electionId)

            elif data_store_key == "District Centre":
                obj = DistrictCentre.create(cell, electionId=election.electionId)

            elif data_store_key == "Counting Centre":
                if election.voteType is VoteTypeEnum.NonPostal:
                    obj = CountingCentre.create(
                        cell, electionId=election.electionId
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.PRE_41, electionId=election.electionId, areaId=obj.areaId
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.CE_201, electionId=election.electionId, areaId=obj.areaId
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.PRE_34_CO, electionId=election.electionId, areaId=obj.areaId
                    )
                elif election.voteType is VoteTypeEnum.Postal:
                    obj = CountingCentre.create(
                        cell, electionId=election.electionId,
                        registeredVotersCount=row["Registered Voters"]
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.PRE_41, electionId=election.electionId, areaId=obj.areaId
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.CE_201_PV, electionId=election.electionId, areaId=obj.areaId
                    )
                    TallySheet.create(
                        tallySheetCode=TallySheetCodeEnum.PRE_34_CO, electionId=election.electionId, areaId=obj.areaId
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
        csv_file_path = csv_path
        if os.path.exists(csv_file_path) is True:
            with open(csv_file_path, 'r') as f:
                reader = csv.DictReader(f, delimiter=',')
                rows = list(reader)
        else:
            rows = []

        # for row in rows:
        #     for cell_key in row:
        #         row[cell_key] = row[cell_key].encode('unicode_escape')

        return rows

    for row in get_rows_from_csv(party_candidate_dataset_file):
        party = get_object(root_election, row, "Party")
        root_election.add_party(partyId=party.partyId)

        candidate = get_object(root_election, row, "Candidate")
        root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

    for row in get_rows_from_csv(invalid_vote_categories_dataset_file):
        root_election.add_invalid_vote_category(row["Invalid Vote Category Description"])

    for row in get_rows_from_csv(polling_station_dataset_file):
        print("[ROW] ========= ", row)
        country = get_object(root_election, {"Country": "Sri Lanka"}, "Country")
        electoralDistrict = get_object(root_election, row, "Electoral District")
        pollingDivision = get_object(root_election, row, "Polling Division")
        pollingDistrict = get_object(root_election, row, "Polling District")
        electionCommission = get_object(root_election, {"Election Commission": "Sri Lanka Election Commission"},
                                        "Election Commission")
        districtCentre = get_object(root_election, row, "District Centre")
        countingCentre = get_object(ordinary_election, row, "Counting Centre")

        registered_voters = row["Registered Voters"]

        pollingStation = get_object(ordinary_election, {
            "Polling Station": row["Polling Station (English)"],
            "Registered Voters": registered_voters
        }, "Polling Station")

        country.add_child(electoralDistrict.areaId)
        electoralDistrict.add_child(pollingDivision.areaId)
        pollingDivision.add_child(pollingDistrict.areaId)
        pollingDistrict.add_child(pollingStation.areaId)
        electionCommission.add_child(districtCentre.areaId)
        districtCentre.add_child(countingCentre.areaId)
        countingCentre.add_child(pollingStation.areaId)

        # stationaryItems = []
        #
        # for i in range(1, 4):
        #     box_key = "Ballot Box %d" % i
        #     if box_key in row and row[box_key] is not None and len(row[box_key]) > 0:
        #         if row[box_key] is not None and len(row[box_key]) > 0:
        #             ballotBox = BallotBox.Model(ballotBoxId=row[box_key], electionId=root_election.electionId)
        #             db.session.add(ballotBox)
        #             stationaryItems.append(ballotBox)
        #             # ballotBox = get_object({"Ballot Box": row[box_key]}, "Ballot Box")
        #
        # if len(row["Ballot - start"]) is not 0 and len(row["Ballot - end"]) is not 0:
        #     for ballotId in range(int(row["Ballot - start"]), int(row["Ballot - end"]) + 1):
        #         ballot = Ballot.Model(ballotId=ballotId, electionId=root_election.electionId)
        #         db.session.add(ballot)
        #         stationaryItems.append(ballot)
        #         # ballot = get_object({"Ballot": str(ballotId)}, "Ballot")
        #         # invoice.add_stationary_item(ballot.stationaryItemId)
        #
        # if len(row["Tendered Ballot - start"]) is not 0 and len(row["Tendered Ballot - end"]) is not 0:
        #     for ballotId in range(int(row["Tendered Ballot - start"]), int(row["Tendered Ballot - end"]) + 1):
        #         ballot = Ballot.Model(ballotId=ballotId, ballotType=BallotTypeEnum.Tendered,
        #                               electionId=root_election.electionId)
        #         db.session.add(ballot)
        #         stationaryItems.append(ballot)
        #         # ballot = get_object({"Tendered Ballot": str(ballotId)}, "Tendered Ballot")
        #         # invoice.add_stationary_item(ballot.stationaryItemId)
        #
        # invoice = Invoice.create(
        #     electionId=root_election.electionId,
        #     issuingOfficeId=countingCentre.areaId,
        #     receivingOfficeId=pollingStation.areaId,
        #     issuedTo=1
        # )
        #
        # invoice.add_stationary_items([stationaryItem.stationaryItemId for stationaryItem in stationaryItems])
        #
        # invoice.set_confirmed()

        print("[ROW END] ========= ")

    for row in get_rows_from_csv(postal_counting_centers_dataset_file):
        print("[POSTAL ROW] ========= ", row)
        country = get_object(root_election, {"Country": "Sri Lanka"}, "Country")
        electoralDistrict = get_object(root_election, row, "Electoral District")
        electionCommission = get_object(root_election, {"Election Commission": "Sri Lanka Election Commission"},
                                        "Election Commission")
        districtCentre = get_object(root_election, row, "District Centre")

        registered_voters = row["Registered Voters"]

        countingCentre = get_object(postal_election, {
            "Counting Centre": row["Postal Vote Counting Centre"], "Registered Voters": registered_voters,
            "Electoral District": row["Electoral District"]
        }, "Counting Centre")

        country.add_child(electoralDistrict.areaId)
        electoralDistrict.add_child(countingCentre.areaId)
        districtCentre.add_child(countingCentre.areaId)
        electionCommission.add_child(districtCentre.areaId)

        print("[POSTAL ROW END] ========= ")

    db.session.commit()

    return root_election

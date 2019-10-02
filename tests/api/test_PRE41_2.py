import requests
import json 
import test_PRE41_1 
import sys
sys.path.insert(1, './jsons/')
import candidates
from random import randrange


##__________________________________________________________________________________________________
## TEST 01 ----  Check all candidates -- Any Tally Sheet ID
def test01(tallySheetID):
    CandidatesList = test_PRE41_1.getCandidateIDs()
    for candidate in CandidatesList:
        response = test_PRE41_1.sendResponseCandidates(tallySheetID,listofCand)
    # print(response.status_code)
    assert response.status_code == 200
    assert len((json.loads(response.text))) > 0

##__________________________________________________________________________________________________
## TEST 02 ----  Check all candidates -- All Tally Sheets

def test02():
    tallySheetList = test_PRE41_1.getTallySheetIDs()
    print(tallySheetList)
    for tID in tallySheetList:
        print("checking TallySheetID  : ", tID)
        test01(tID)
    return



##__________________________________________________________________________________________________
## TEST 03 ----  Check all candidates -- All Tally Sheets --> Create tally sheet version
def test03():
    # createTallySheetVersion(tID,candidateId,count,countInWords,rejVotes)
    
    #tallySheetIds
    tallySheetList = test_PRE41_1.getTallySheetIDs()
    CandidatesList = test_PRE41_1.getCandidateIDs()

    for tID in tallySheetList:
        print("Checking for TallySheet ID: ",tID)
        for cID in CandidatesList:
            print("Checking for Candidate: ",cID)
            createTallySheet = test_PRE41_1.createTallySheetVersion(tID,cID,20,"Twenty",0) 
            assert createTallySheet.status_code == 200
            assert len((json.loads(createTallySheet.text))) > 0

    return




##__________________________________________________________________________________________________
## TEST 04 ----  Create tally sheet version -- Zero for Tally Sheet ID and zero for Candidate ID
def test04():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(0,0,20,"Twenty",0)
    assert createTallySheetRes.status_code == 404
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 05 ----  Create tally sheet version -- Zero as candidate ID
def test05():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,0,20,"Twenty",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 06 ----  Create tally sheet version --> Negative values for Rejected Votes
def test06():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,1,20,"Twenty",-1)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 07 ----  Create tally sheet version --> Blank for Count in Words
def test07():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,1,20,"",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 08 ----  Create tally sheet version --> Negative Value for Count
def test08():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,1,-1,"Negative One",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 09 ----  Create tally sheet version --> Invalid TallySheetID
def test09():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(1000,19,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 404
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 10 ----  Create tally sheet version --> Invalid Candidate ID
def test10():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,190000,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 11 ----  Create tally sheet version --> Negative Candidate ID
def test11():
    createTallySheetRes = test_PRE41_1.createTallySheetVersion(145,-19,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return




test09()
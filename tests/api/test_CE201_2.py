import requests
import json 
import test_CE201_1

# TEST 01 Test default code for all area IDs
##______________________________________________________________________________________________________
def test01():
    tallySheetList = test_CE201_1.getTallySheetIDs("CE-201")
    areaDict = test_CE201_1.getAreaIDs()
    for tallySheet in tallySheetList:            
        for area in areaDict:
            areaId = area["areaId"]
            electionId = area["electionId"]
            if electionId==1:
                print("checking for tallySheet ID: ", tallySheet, " and area ID: ",areaId)
                CE201Response = test_CE201_1.createTallySheetVersion("CE-201",tallySheet,areaId,["String"],["String"],0, 0, 0, 0, 0, 0, 0,0  )
                assert CE201Response.status_code == 200
                assert len((json.loads(CE201Response.text))) > 0


    return




# TEST 02 Test multiple ballot box ids as list of string
##______________________________________________________________________________________________________
def test02():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1","String2","String3","String4","String5","String6"],0, 0, 0, 0, 0, 0, 0,0  )
    assert CE201Response.status_code == 200
    assert len((json.loads(CE201Response.text))) > 0
    return


# TEST 03 Multiple ballotbox ids with duplicates
##______________________________________________________________________________________________________
def test03():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,1,["String1","String1","String3","String4","String5","String6"],["String1"],0, 0, 0, 0, 0, 0, 0,0  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 500
    assert len((json.loads(CE201Response.text))) > 0
    return



# TEST 04 Negative Values for ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused, ordinaryBallotCountFromBallotPaperAccount, etc.
##______________________________________________________________________________________________________
def test04():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 500
    assert len((json.loads(CE201Response.text))) > 0
    return



# TEST 05 Invalid Area Id
##______________________________________________________________________________________________________
def test05():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,830,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 404
    assert len((json.loads(CE201Response.text))) > 0
    return


# TEST 06 Check if tallySheetID is returned in the response with the version id which should be included in the contentUrl
##______________________________________________________________________________________________________
def test06():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90)
    ceRes = json.loads(CE201Response.text)
    tallySheetId = ceRes["tallySheetId"]
    tallySheetVersionId = ceRes["tallySheetVersionId"]
    contentUrl = ceRes["contentUrl"]

    assert int(tallySheetId) ==132
    assert isinstance(tallySheetVersionId, int) == True
    assert (str(tallySheetId) in contentUrl)==True       
    assert (str(tallySheetVersionId) in contentUrl)==True

    return





# TEST 07 Loop test 6 for all Tally Sheets and area IDs
##______________________________________________________________________________________________________
def test07():
    tallySheetList = test_CE201_1.getTallySheetIDs("CE-201")
    areaDict = test_CE201_1.getAreaIDs()

    for tiD in tallySheetList:
        for area in areaDict:
            areaId = area["areaId"]
            electionId = area["electionId"]
            if electionId==1:
                print("Checking TallySheetID : ", tiD," and area ID: ", areaId)
                CE201Response = test_CE201_1.createTallySheetVersion("CE-201",tiD,areaId,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90)
                ceRes = json.loads(CE201Response.text)
                tallySheetId = ceRes["tallySheetId"]
                tallySheetVersionId = ceRes["tallySheetVersionId"]
                contentUrl = ceRes["contentUrl"]

                assert int(tallySheetId) ==132
                assert isinstance(tallySheetVersionId, int) == True
                assert (str(tallySheetId) in contentUrl)==True       
                assert (str(tallySheetVersionId) in contentUrl)==True

    return


# TEST 08 Leave ballotBoxesIssued / ballotBoxesReceived Blank
##______________________________________________________________________________________________________
def test08():
    CE201Response = test_CE201_1.createTallySheetVersion("CE-201",132,2,[],[],10, 20, 30, 400, 10, 30, 40,90)
    print(CE201Response.status_code)
    assert CE201Response.status_code == 200
    assert len((json.loads(CE201Response.text))) > 0

    return



test08()

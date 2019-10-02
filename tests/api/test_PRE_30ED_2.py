import requests
import json 
import test_PRE_30ED_1


##_________________________________________________________________________________________________________________
#   TEST 01 -- Check for all tallySheetIds if returns for tallySheetId, tallySheetVersionId and contentUrl and it contains the info
def test01():
    code = "PRE-30-ED"
    tallySheetList = test_PRE_30_1.getTallySheetIDs(code)
    for tallySheet in tallySheetList:
        print("Checking for tally sheet id: ", tallySheet)
        response = test_PRE_30_1.createTallySheetVersion(code,tallySheet)

        resContent = json.loads(response.text)

        print('Checking if response returned the correct tallysheet iID')
        assert int(resContent['tallySheetId']) ==tallySheet
        print('Checking if response contains the tallysheet version which is an integer')
        assert isinstance(resContent['tallySheetVersionId'], int) == True
        print('Checking if response URL contains tallysheet ID and tallysheetID version')
        assert (str(resContent['tallySheetId']) in resContent['contentUrl'])==True       
        assert (str(resContent['tallySheetVersionId']) in resContent['contentUrl'])==True
        print("Checking if response returned 200 and body contains characters")
        assert response.status_code == 200
        assert len((json.loads(response.text))) > 0


    return




##_________________________________________________________________________________________________________________
#   TEST 02 -- Loop any tally sheetID for five times and check if versions numbers are changed
def test02(tID):
    code = "PRE-30-ED"
    reportedVersions = []

    for ver in range(5):
        print(ver,"th iternation to check")
        response = test_PRE_30_1.createTallySheetVersion(code,tID)
        resContent = json.loads(response.text)
        verID= resContent['tallySheetVersionId']
        assert (verID in reportedVersions)==False
        reportedVersions.append(verID)      


    return reportedVersions



##_________________________________________________________________________________________________________________
#   TEST 03 -- Loop through all tally sheets and Loop any tally sheetID for five times and check if versions numbers are changed
def test03():
    code = "PRE-30-ED"
    tallySheetList = test_PRE_30_1.getTallySheetIDs(code)
    for tallySheet in tallySheetList:          

        reportedVersions = []

        for ver in range(5):
            print("Checking TID :",tallySheet)

            print(ver,"th iternation to check")
            response = test_PRE_30_1.createTallySheetVersion(code,tallySheet)
            resContent = json.loads(response.text)
            verID= resContent['tallySheetVersionId']
            assert (verID in reportedVersions)==False
            reportedVersions.append(verID)      


    return reportedVersions




tallySheetCodes = ["PRE-30-ED","PRE-30-PD"]



# test01(tallySheetCodes[0])
# test03(tallySheetCodes[0])
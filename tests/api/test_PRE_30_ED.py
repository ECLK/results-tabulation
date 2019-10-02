import requests
import json 

## Get tallySheetIDs
def getTallySheetIDs():
    code = "PRE-30-ED"
    tallySheetIdList = []
    url = "http://localhost:5000/tally-sheet"
    querystring = {"tallySheetCode":code}
    
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
        'cache-control': "no-cache",
        'Postman-Token': "6071fd7b-2b32-4e12-9c71-1d5022e1bda4"
            }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    tallyRes = json.loads(response.text)
    for tallyID in tallyRes:
        tallySheetId = tallyID['tallySheetId']
        tallySheetIdList.append(tallySheetId)
    return tallySheetIdList




def createTallySheetVersion(tID):
    code = "PRE-30-ED"
    url = "http://localhost:5000/tally-sheet/"+code+"/"+str(tID)+"/version"
    payload = ""
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
    'cache-control': "no-cache",
    'Postman-Token': "6a8b209a-ae6f-4e05-94ce-0145c58140be"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response




##_====================================================================================
# TEST CASES BELOW


##_________________________________________________________________________________________________________________
#   TEST 01 -- Check for all tallySheetIds if returns for tallySheetId, tallySheetVersionId and contentUrl and it contains the info
def test01():
    code = "PRE-30-ED"
    tallySheetList = getTallySheetIDs(code)
    for tallySheet in tallySheetList:
        print("Checking for tally sheet id: ", tallySheet)
        response = createTallySheetVersion(code,tallySheet)

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
        response = createTallySheetVersion(code,tID)
        resContent = json.loads(response.text)
        verID= resContent['tallySheetVersionId']
        assert (verID in reportedVersions)==False
        reportedVersions.append(verID)      


    return reportedVersions



##_________________________________________________________________________________________________________________
#   TEST 03 -- Loop through all tally sheets and Loop any tally sheetID for five times and check if versions numbers are changed
def test03():
    code = "PRE-30-ED"
    tallySheetList = getTallySheetIDs(code)
    for tallySheet in tallySheetList:          

        reportedVersions = []

        for ver in range(5):
            print("Checking TID :",tallySheet)

            print(ver,"th iternation to check")
            response = createTallySheetVersion(code,tallySheet)
            resContent = json.loads(response.text)
            verID= resContent['tallySheetVersionId']
            assert (verID in reportedVersions)==False
            reportedVersions.append(verID)      


    return reportedVersions


import requests
import json 

## Get tallySheetIDs
def getTallySheetIDs(code):
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


def getAreaIDs():
    url = "http://localhost:5000/area"
    payload = ""
    headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
            'cache-control': "no-cache",
            'Postman-Token': "16c078c2-d0b7-4b81-aab1-3efb670e72b7"
            }

    response = requests.request("GET", url, data=payload, headers=headers)
    areaInfo = json.loads(response.text)
    return areaInfo



def createTallySheetVersion(code,tID,areaID,blttBxIsd,blttBxRvd,bltIsd, blttRvd, blttSplt, blttUnsd, ordBltCntBltPAcc, ordBltCntBxCnt, tndrdBltCntBltPAc,tndrdBltCntBxCnt):
    url = "http://localhost:5000/tally-sheet/"+code+"/"+str(tID)+"/version"
    bdyJsn = dict()
    contentList = []
    contentItem = dict()
    contentItem["areaId"] = areaID
    contentItem["ballotBoxesIssued"] = blttBxIsd
    contentItem["ballotBoxesReceived"] = blttBxRvd
    contentItem["ballotsIssued"] = bltIsd
    contentItem["ballotsReceived"] = blttRvd
    contentItem["ballotsSpoilt"] = blttSplt
    contentItem["ballotsUnused"] = blttUnsd
    contentItem["ordinaryBallotCountFromBallotPaperAccount"] = ordBltCntBltPAcc
    contentItem["ordinaryBallotCountFromBoxCount"] = ordBltCntBxCnt
    contentItem["tenderedBallotCountFromBallotPaperAccount"] = tndrdBltCntBltPAc
    contentItem["tenderedBallotCountFromBoxCount"] = tndrdBltCntBxCnt

    contentList.append(contentItem)
    bdyJsn['content'] = contentList
    payload = json.dumps(bdyJsn)
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
    'cache-control': "no-cache",
    'Postman-Token': "6a8b209a-ae6f-4e05-94ce-0145c58140be"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response


# print(getTallySheetIDs("CE-201"))
# print(getTallySheetIDs("CE-201-PV"))


# print(createTallySheetVersion("CE-201","132",1,["String"],["String"],0, 0, 0, 0, 0, 0, 0,0  ))

# print(getAreaIDs())




## ==============================================================================

##TEST CASES BELOW

# TEST 01 Test default code for all area IDs
##______________________________________________________________________________________________________
def test01():
    tallySheetList = getTallySheetIDs("CE-201")
    areaDict = getAreaIDs()
    for tallySheet in tallySheetList:            
        for area in areaDict:
            areaId = area["areaId"]
            electionId = area["electionId"]
            if electionId==1:
                print("checking for tallySheet ID: ", tallySheet, " and area ID: ",areaId)
                CE201Response = createTallySheetVersion("CE-201",tallySheet,areaId,["String"],["String"],0, 0, 0, 0, 0, 0, 0,0  )
                assert CE201Response.status_code == 200
                assert len((json.loads(CE201Response.text))) > 0


    return




# TEST 02 Test multiple ballot box ids as list of string
##______________________________________________________________________________________________________
def test02():
    CE201Response = createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1","String2","String3","String4","String5","String6"],0, 0, 0, 0, 0, 0, 0,0  )
    assert CE201Response.status_code == 200
    assert len((json.loads(CE201Response.text))) > 0
    return


# TEST 03 Multiple ballotbox ids with duplicates
##______________________________________________________________________________________________________
def test03():
    CE201Response = createTallySheetVersion("CE-201",132,1,["String1","String1","String3","String4","String5","String6"],["String1"],0, 0, 0, 0, 0, 0, 0,0  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 500
    assert len((json.loads(CE201Response.text))) > 0
    return



# TEST 04 Negative Values for ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused, ordinaryBallotCountFromBallotPaperAccount, etc.
##______________________________________________________________________________________________________
def test04():
    CE201Response = createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 500
    assert len((json.loads(CE201Response.text))) > 0
    return



# TEST 05 Invalid Area Id
##______________________________________________________________________________________________________
def test05():
    CE201Response = createTallySheetVersion("CE-201",132,830,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90  )
    print(CE201Response.status_code)
    assert CE201Response.status_code == 404
    assert len((json.loads(CE201Response.text))) > 0
    return


# TEST 06 Check if tallySheetID is returned in the response with the version id which should be included in the contentUrl
##______________________________________________________________________________________________________
def test06():
    CE201Response = createTallySheetVersion("CE-201",132,1,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90)
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
    tallySheetList = getTallySheetIDs("CE-201")
    areaDict = getAreaIDs()

    for tiD in tallySheetList:
        for area in areaDict:
            areaId = area["areaId"]
            electionId = area["electionId"]
            if electionId==1:
                print("Checking TallySheetID : ", tiD," and area ID: ", areaId)
                CE201Response = createTallySheetVersion("CE-201",tiD,areaId,["String1","String2","String3","String4","String5","String6"],["String1"],10, 20, 30, 400, 10, 30, 40,90)
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
    CE201Response = createTallySheetVersion("CE-201",132,2,[],[],10, 20, 30, 400, 10, 30, 40,90)
    print(CE201Response.status_code)
    assert CE201Response.status_code == 200
    assert len((json.loads(CE201Response.text))) > 0

    return


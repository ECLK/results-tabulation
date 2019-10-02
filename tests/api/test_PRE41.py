import requests
import json 



def getURL(tallySheetID):
    urlNew  ="http://localhost:5000/tally-sheet/PRE-41/"+str(tallySheetID)+"/version"
    return urlNew


def getPayload(listofCand):
    payload = dict()
    payload["content"] = listofCand
    payOut = json.dumps(payload)
    return payOut
    

def getResponse(url,payload):
    headers = {
            'Accept': "application/json",
            'Content-Type': "application/json"
                }
    response = requests.request("POST", url, data=payload, headers=headers)

    return response


def sendResponseCandidates(tallySheetID,listofCand):
    res = getResponse(getURL(tallySheetID), (listofCand))
    return res







def createTallySheetVersion(tID,candidateId,count,countInWords,rejVotes):

    url = "http://localhost:5000/tally-sheet/PRE-41/"+str(tID)+"/version"
    postDict = dict()

    contentList = []
    candDict = dict()
    candDict['candidateId'] = candidateId
    candDict['count'] = count
    candDict['countInWords'] = countInWords
    contentList.append(candDict)

    postDict['content'] = contentList
    rejVotDict = dict()
    rejVotDict['rejectedVoteCount'] = rejVotes

    postDict['summary'] = rejVotDict

    payload = json.dumps(postDict)    

    headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
            'cache-control': "no-cache",
            'Postman-Token': "1e4d0dc1-31d5-417d-a4f2-7b1f164eb5ab"
            }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response





## Get TallySheetIDs for PRE41
def getTallySheetIDs():
    tIDList = []
    url = "http://localhost:5000/tally-sheet"
    querystring = {"limit":"20","offset":"0","tallySheetCode":"PRE-41"}
    payload = ""
    headers = {
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
    'cache-control': "no-cache",
    'Postman-Token': "4dac8955-5bd2-4a05-a6af-437654de5102"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    out = json.loads(response.text)

    for tallyInfo in out:
        tID = tallyInfo['tallySheetId']
        tIDList.append(tID)


    return tIDList






def getCandidateIDs():
    candIds = []
    url = "http://localhost:5000/election"

    payload = ""
    headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcmVhQXNzaWdubWVudC9kYXRhRWRpdG9yIjpbeyJhcmVhSWQiOjcsImFyZWFOYW1lIjoiMSJ9LHsiYXJlYUlkIjoxMCwiYXJlYU5hbWUiOiIyIn0seyJhcmVhSWQiOjEzLCJhcmVhTmFtZSI6IjQifSx7ImFyZWFJZCI6MTYsImFyZWFOYW1lIjoiMyJ9LHsiYXJlYUlkIjoxOSwiYXJlYU5hbWUiOiI2In0seyJhcmVhSWQiOjIyLCJhcmVhTmFtZSI6IjUifSx7ImFyZWFJZCI6MjUsImFyZWFOYW1lIjoiNyJ9LHsiYXJlYUlkIjozMiwiYXJlYU5hbWUiOiI4In0seyJhcmVhSWQiOjY0LCJhcmVhTmFtZSI6IjkifSx7ImFyZWFJZCI6MTc1LCJhcmVhTmFtZSI6IjEwIn0seyJhcmVhSWQiOjE3OCwiYXJlYU5hbWUiOiIxMSJ9LHsiYXJlYUlkIjoxODMsImFyZWFOYW1lIjoiMTMifSx7ImFyZWFJZCI6MTg2LCJhcmVhTmFtZSI6IjEyIn0seyJhcmVhSWQiOjE5MywiYXJlYU5hbWUiOiIxNCJ9LHsiYXJlYUlkIjoxOTYsImFyZWFOYW1lIjoiMTYifSx7ImFyZWFJZCI6MjEzLCJhcmVhTmFtZSI6IjE1In0seyJhcmVhSWQiOjIxOCwiYXJlYU5hbWUiOiIxNyJ9LHsiYXJlYUlkIjozNjgsImFyZWFOYW1lIjoiMjUifSx7ImFyZWFJZCI6MzczLCJhcmVhTmFtZSI6IjE4In0seyJhcmVhSWQiOjM3OCwiYXJlYU5hbWUiOiIyMCJ9LHsiYXJlYUlkIjozODEsImFyZWFOYW1lIjoiMjMifSx7ImFyZWFJZCI6Mzg0LCJhcmVhTmFtZSI6IjIyIn0seyJhcmVhSWQiOjM4OSwiYXJlYU5hbWUiOiIyNCJ9LHsiYXJlYUlkIjozOTQsImFyZWFOYW1lIjoiMTkifSx7ImFyZWFJZCI6NDA1LCJhcmVhTmFtZSI6IjIxIn0seyJhcmVhSWQiOjU0MywiYXJlYU5hbWUiOiIyNiJ9LHsiYXJlYUlkIjo1NDgsImFyZWFOYW1lIjoiMjcifSx7ImFyZWFJZCI6NTUxLCJhcmVhTmFtZSI6IjI4In0seyJhcmVhSWQiOjU1NCwiYXJlYU5hbWUiOiIyOSJ9LHsiYXJlYUlkIjo1NTcsImFyZWFOYW1lIjoiMzAifSx7ImFyZWFJZCI6NTYwLCJhcmVhTmFtZSI6IjMxIn0seyJhcmVhSWQiOjU3NywiYXJlYU5hbWUiOiIzMiJ9LHsiYXJlYUlkIjo2ODAsImFyZWFOYW1lIjoiMzMifSx7ImFyZWFJZCI6NjgzLCJhcmVhTmFtZSI6IjM0In0seyJhcmVhSWQiOjY4OCwiYXJlYU5hbWUiOiIzNSJ9LHsiYXJlYUlkIjo2OTEsImFyZWFOYW1lIjoiMzYifSx7ImFyZWFJZCI6Njk2LCJhcmVhTmFtZSI6IjM3In0seyJhcmVhSWQiOjcxMywiYXJlYU5hbWUiOiIzOCJ9LHsiYXJlYUlkIjo3MTgsImFyZWFOYW1lIjoiNDAifSx7ImFyZWFJZCI6NzM5LCJhcmVhTmFtZSI6IjM5In0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MSJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDIifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQzIn0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NCJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDUifSx7ImFyZWFJZCI6ODQzLCJhcmVhTmFtZSI6IlBWIDQ2In1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRWaWV3ZXIiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9wb2xsaW5nRGl2aXNpb25SZXBvcnRHZW5lcmF0b3IiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifSx7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9lbGVjdG9yYWxEaXN0cmljdFJlcG9ydEdlbmVyYXRvciI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhQXNzaWdubWVudC9uYXRpb25hbFJlcG9ydFZpZXdlciI6W3siYXJlYUlkIjoxLCJhcmVhTmFtZSI6IlNyaSBMYW5rYSJ9XSwiYXJlYUFzc2lnbm1lbnQvRUNMZWFkZXJzaGlwIjpbXX0.15bYz1mPtuP1JI6jhb6vPPMcndwAkrfryC_NElI0l4s",
        'cache-control': "no-cache",
        'Postman-Token': "df8274ae-ee92-44e2-acb1-cc5e5cea5735"
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    electionsList  = json.loads(response.text)

    electionsList  = json.loads(response.text)
    for election in electionsList:
        partiesList = election['parties']
        for party in partiesList:
                candidatesList = party['candidates']
                for candidateInfo in candidatesList:
                    candidateID = candidateInfo['candidateId']
                    candIds.append(candidateID)
    return candIds





##=========================================================================================
#TEST CASES BELOW


##__________________________________________________________________________________________________
## TEST 01 ----  Check all candidates -- Any Tally Sheet ID
def test01(tallySheetID):
    CandidatesList = getCandidateIDs()
    for candidate in CandidatesList:
        response = sendResponseCandidates(tallySheetID,listofCand)
    # print(response.status_code)
    assert response.status_code == 200
    assert len((json.loads(response.text))) > 0

##__________________________________________________________________________________________________
## TEST 02 ----  Check all candidates -- All Tally Sheets

def test02():
    tallySheetList = getTallySheetIDs()
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
    tallySheetList = getTallySheetIDs()
    CandidatesList = getCandidateIDs()

    for tID in tallySheetList:
        print("Checking for TallySheet ID: ",tID)
        for cID in CandidatesList:
            print("Checking for Candidate: ",cID)
            createTallySheet = createTallySheetVersion(tID,cID,20,"Twenty",0) 
            assert createTallySheet.status_code == 200
            assert len((json.loads(createTallySheet.text))) > 0

    return




##__________________________________________________________________________________________________
## TEST 04 ----  Create tally sheet version -- Zero for Tally Sheet ID and zero for Candidate ID
def test04():
    createTallySheetRes = createTallySheetVersion(0,0,20,"Twenty",0)
    assert createTallySheetRes.status_code == 404
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 05 ----  Create tally sheet version -- Zero as candidate ID
def test05():
    createTallySheetRes = createTallySheetVersion(145,0,20,"Twenty",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 06 ----  Create tally sheet version --> Negative values for Rejected Votes
def test06():
    createTallySheetRes = createTallySheetVersion(145,1,20,"Twenty",-1)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 07 ----  Create tally sheet version --> Blank for Count in Words
def test07():
    createTallySheetRes = createTallySheetVersion(145,1,20,"",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 08 ----  Create tally sheet version --> Negative Value for Count
def test08():
    createTallySheetRes = createTallySheetVersion(145,1,-1,"Negative One",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 09 ----  Create tally sheet version --> Invalid TallySheetID
def test09():
    createTallySheetRes = createTallySheetVersion(1000,19,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 404
    assert len((json.loads(createTallySheetRes.text))) > 0

    return



##__________________________________________________________________________________________________
## TEST 10 ----  Create tally sheet version --> Invalid Candidate ID
def test10():
    createTallySheetRes = createTallySheetVersion(145,190000,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


##__________________________________________________________________________________________________
## TEST 11 ----  Create tally sheet version --> Negative Candidate ID
def test11():
    createTallySheetRes = createTallySheetVersion(145,-19,1000,"One Thousand",0)
    assert createTallySheetRes.status_code == 500
    assert len((json.loads(createTallySheetRes.text))) > 0

    return


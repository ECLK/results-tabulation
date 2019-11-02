import pytest
import requests


class TestPre34Class:
    rootUrl = "http://0.0.0.0:5000"
    headers = {"accept": "application/json",
               "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqYW5ha0BjYXJib24uc3VwZXIiLCJ1c2VyQWNjZXNzQXJlYUlkcyI6WzE1XSwiYXJlYV9hc3NpZ25fZGF0YV9lZGl0b3IiOlt7ImFyZWFJZCI6ODM3LCJhcmVhTmFtZSI6IlBWIDQxIn0seyJhcmVhSWQiOjgzOCwiYXJlYU5hbWUiOiJQViA0MiJ9LHsiYXJlYUlkIjo4MzksImFyZWFOYW1lIjoiUFYgNDMifSx7ImFyZWFJZCI6ODQwLCJhcmVhTmFtZSI6IlBWIDQ0In0seyJhcmVhSWQiOjg0MSwiYXJlYU5hbWUiOiJQViA0NSJ9LHsiYXJlYUlkIjo4NDIsImFyZWFOYW1lIjoiUFYgNDYifSx7ImFyZWFJZCI6NywiYXJlYU5hbWUiOiIxIn0seyJhcmVhSWQiOjE0LCJhcmVhTmFtZSI6IjQwIn0seyJhcmVhSWQiOjEwLCJhcmVhTmFtZSI6IjIifSx7ImFyZWFJZCI6MTMsImFyZWFOYW1lIjoiNCJ9LHsiYXJlYUlkIjoxNiwiYXJlYU5hbWUiOiIzIn0seyJhcmVhSWQiOjE5LCJhcmVhTmFtZSI6IjYifSx7ImFyZWFJZCI6MjIsImFyZWFOYW1lIjoiNSJ9LHsiYXJlYUlkIjoyNSwiYXJlYU5hbWUiOiI3In0seyJhcmVhSWQiOjMyLCJhcmVhTmFtZSI6IjgifSx7ImFyZWFJZCI6NjQsImFyZWFOYW1lIjoiOSJ9LHsiYXJlYUlkIjoxNzUsImFyZWFOYW1lIjoiMTAifSx7ImFyZWFJZCI6MTc4LCJhcmVhTmFtZSI6IjExIn0seyJhcmVhSWQiOjE4MywiYXJlYU5hbWUiOiIxMyJ9LHsiYXJlYUlkIjoxODYsImFyZWFOYW1lIjoiMTIifSx7ImFyZWFJZCI6MTkzLCJhcmVhTmFtZSI6IjE0In0seyJhcmVhSWQiOjE5NiwiYXJlYU5hbWUiOiIxNiJ9LHsiYXJlYUlkIjoyMTMsImFyZWFOYW1lIjoiMTUifSx7ImFyZWFJZCI6MjE4LCJhcmVhTmFtZSI6IjE3In0seyJhcmVhSWQiOjM2OCwiYXJlYU5hbWUiOiIyNSJ9LHsiYXJlYUlkIjozNzMsImFyZWFOYW1lIjoiMTgifSx7ImFyZWFJZCI6Mzc4LCJhcmVhTmFtZSI6IjIwIn0seyJhcmVhSWQiOjM4MSwiYXJlYU5hbWUiOiIyMyJ9LHsiYXJlYUlkIjozODQsImFyZWFOYW1lIjoiMjIifSx7ImFyZWFJZCI6Mzg5LCJhcmVhTmFtZSI6IjI0In0seyJhcmVhSWQiOjM5NCwiYXJlYU5hbWUiOiIxOSJ9LHsiYXJlYUlkIjo0MDUsImFyZWFOYW1lIjoiMjEifSx7ImFyZWFJZCI6NTQzLCJhcmVhTmFtZSI6IjI2In0seyJhcmVhSWQiOjU0OCwiYXJlYU5hbWUiOiIyNyJ9LHsiYXJlYUlkIjo1NTEsImFyZWFOYW1lIjoiMjgifSx7ImFyZWFJZCI6NTU0LCJhcmVhTmFtZSI6IjI5In0seyJhcmVhSWQiOjU1NywiYXJlYU5hbWUiOiIzMCJ9LHsiYXJlYUlkIjo1NjAsImFyZWFOYW1lIjoiMzEifSx7ImFyZWFJZCI6NTc3LCJhcmVhTmFtZSI6IjMyIn0seyJhcmVhSWQiOjY4MCwiYXJlYU5hbWUiOiIzMyJ9LHsiYXJlYUlkIjo2ODMsImFyZWFOYW1lIjoiMzQifSx7ImFyZWFJZCI6Njg4LCJhcmVhTmFtZSI6IjM1In0seyJhcmVhSWQiOjY5MSwiYXJlYU5hbWUiOiIzNiJ9LHsiYXJlYUlkIjo2OTYsImFyZWFOYW1lIjoiMzcifSx7ImFyZWFJZCI6NzEzLCJhcmVhTmFtZSI6IjM4In0seyJhcmVhSWQiOjcxOCwiYXJlYU5hbWUiOiI0MCJ9LHsiYXJlYUlkIjo3MzksImFyZWFOYW1lIjoiMzkifV0sImFyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZpZXciOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifV0sImFyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZlcmYiOlt7ImFyZWFJZCI6MywiYXJlYU5hbWUiOiJBLVB1dHRhbGFtIn0seyJhcmVhSWQiOjE3MywiYXJlYU5hbWUiOiJCLUFuYW1hZHV3YSJ9LHsiYXJlYUlkIjozNjYsImFyZWFOYW1lIjoiQy1DaGlsYXcifSx7ImFyZWFJZCI6NTQxLCJhcmVhTmFtZSI6IkQtTmF0aHRoYW5kaXlhIn0seyJhcmVhSWQiOjY3OCwiYXJlYU5hbWUiOiJFLVdlbm5hcHB1d2EifV0sImFyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZpZXciOlt7ImFyZWFJZCI6MiwiYXJlYU5hbWUiOiJQdXR0YWxhbSJ9XSwiYXJlYV9hc3NpZ25fZWxjX2Rpc19yZXBfdmVyZiI6W3siYXJlYUlkIjoyLCJhcmVhTmFtZSI6IlB1dHRhbGFtIn1dLCJhcmVhX2Fzc2lnbl9uYXRfZGlzX3JlcF92aWV3IjpbXSwiYXJlYV9hc3NpZ25fbmF0X2Rpc19yZXBfdmVyZiI6W10sImFyZWFfYXNzaWduX2VjX2xlYWRlcnNoaXAiOltdfQ.9_eG0ZxAydgBK3EzxtewDbMYJFa0s2WcDtF007Zz7CQ"
               }

    def test_pre_34_co_post(self):
        request_payload = {
            "content": [
                {
                    "candidateId": 1,
                    "notCountedBallotPapers": 65,
                    "preferences": [
                        {
                            "candidateId": 10,
                            "no2rdPreferences": 1000,
                            "no3rdPreferences": 3000
                        }
                    ],
                    "remainingBallotPapers": 45
                }
            ]
        }
        response = requests.post(self.rootUrl + "/tally-sheet/PRE-34-CO/12/version",
                                 json=request_payload, headers=self.headers)
        assert response.ok

    def test_buttons2(self):
        # self.$attribute can be used, but not cls.$attribute?
        pass

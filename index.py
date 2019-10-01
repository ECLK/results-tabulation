import app
from jose import jwt

key = "jwt_secret"
payload = {
    'areaAssignment/dataEditor': [
        {
            "areaName": "1",
            "areaId": 7
        }
    ],
    'areaAssignment/ECLeadership': [
    ]
}
encoded = jwt.encode(payload, key)
print("""

JWT_TOKEN = %s

""" % encoded)

if __name__ == "__main__":
    connex_app = app.create_app()
    connex_app.run(debug=connex_app.app.config['DEBUG'])

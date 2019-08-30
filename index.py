from app import connex_app
from flask_cors import CORS

if __name__ == "__main__":
    # add CORS support
    CORS(connex_app.app)

    connex_app.run(debug=connex_app.app.config['DEBUG'])

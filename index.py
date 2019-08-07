from app import connex_app

if __name__ == "__main__":
    connex_app.run(debug=connex_app.app.config['DEBUG'], ssl_context='adhoc')

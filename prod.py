from app import connex_app

if __name__ == "__main__":
    connex_app.run(debug=True, ssl_context=('./ssl/prod/cert.pem', './ssl/prod/key.pem'))

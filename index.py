import app

if __name__ == "__main__":
    connex_app = app.create_app()
    connex_app.run(debug=connex_app.app.config['DEBUG'])

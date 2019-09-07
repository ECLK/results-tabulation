import pytest

from app import create_app, db


@pytest.fixture(scope="session")
def test_client():
    connex_app = create_app()
    flask_app = connex_app.app
    tc = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        db.session.commit()

        from build_database import build_database
        build_database('test-small')

        yield tc

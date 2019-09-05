import pytest

from app import create_app


@pytest.fixture(scope='session')
def test_client():
    connex_app = create_app()
    flask_app = connex_app.app
    tc = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield tc
    ctx.pop()

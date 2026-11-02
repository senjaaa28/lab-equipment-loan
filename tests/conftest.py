import pytest

from app import create_app
from app.database import init_db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "lab_equipment_test.db"
    application = create_app(
        {"DATABASE": str(database_path), "TESTING": True}
    )
    with application.app_context():
        init_db()
    yield application


@pytest.fixture
def client(app):
    return app.test_client()

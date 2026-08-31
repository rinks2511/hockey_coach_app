import os
import tempfile
import pytest
from fastapi.testclient import TestClient

# Mock database file to use a temporary DB path during tests
# Must set this BEFORE importing database/main modules
TEST_DB_PATH = tempfile.mktemp(suffix=".db")
os.environ["DATABASE_FILE"] = TEST_DB_PATH

from backend.app.database import init_db
from backend.app.main import app, get_current_coach_email

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    init_db()
    yield
    # Clean up test DB file after testing completes
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except OSError:
            pass

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_coach():
    def _mock(team_id: str):
        return "singhalrajeev89@gmail.com"
    return _mock

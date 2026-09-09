import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(
        app,
        headers={"X-API-Key": "dev-secret-key-123"}
    ) as test_client:
        yield test_client
"""Fixtures pytest."""

import pytest
from fastapi.testclient import TestClient

from eurocode_calculator.main import create_app


@pytest.fixture
def client():
    return TestClient(create_app())

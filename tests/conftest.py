import sys
from copy import deepcopy
from pathlib import Path

import pytest

# Ensure the src directory is importable when running tests from repo root
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities between tests to avoid cross-test coupling."""
    from app import activities

    snapshot = deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(deepcopy(snapshot))


@pytest.fixture()
def client():
    from app import app
    from fastapi.testclient import TestClient

    return TestClient(app)

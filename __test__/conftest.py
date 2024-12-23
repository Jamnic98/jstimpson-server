import os
import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from main import app


@pytest.fixture(scope="function", autouse=True)
def reset_env():
    # Save the original environment variable
    original_env = os.environ.get("ENV")
    # Set to "test" for testing
    os.environ["ENV"] = "test"
    yield
    # Restore the original environment variable
    if original_env:
        os.environ["ENV"] = original_env
    else:
        del os.environ["ENV"]

@pytest.fixture(scope="function", autouse=True)
def override_get_settings():
    def get_settings_override():
        return Settings()

    app.dependency_overrides[get_settings] = get_settings_override
    yield
    # Reset overrides after each test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client():
    return TestClient(app)

from fastapi.testclient import TestClient

# from app.config import Settings, get_settings
from main import app

client = TestClient(app)


# def get_settings_override():
#     return Settings()
#
#
# app.dependency_overrides[get_settings] = get_settings_override

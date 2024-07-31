from app.core.models.strava_token_model import StravaTokenModel
from .data.strava_tokens import test_strava_tokens


def test_is_token_valid():
    #  test expired token
    expired_token_data = test_strava_tokens["expired_token"]
    test_token = StravaTokenModel.model_validate(expired_token_data)
    assert test_token.is_token_valid() is False

    # test valid token
    valid_token_data = test_strava_tokens["valid_token"]
    test_token = StravaTokenModel.model_validate(valid_token_data)
    assert test_token.is_token_valid() is True

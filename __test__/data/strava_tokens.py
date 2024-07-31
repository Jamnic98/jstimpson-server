from datetime import datetime

test_strava_tokens = {
    "expired_token": {
        "token_type": "Bearer",
        "access_token": "expired_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": 123456,
        "expires_in": 1000
    },
    "valid_token": {
        "token_type": "Bearer",
        "access_token": "valid_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": datetime.timestamp(datetime(3000, 1, 1)),
        "expires_in": 1e10
    }
}

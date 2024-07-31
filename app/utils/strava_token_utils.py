from requests import post, HTTPError

from app.factories.logger import logger
from app.utils import STRAVA_TOKEN_API_ENDPOINT
from app.config import settings


async def fetch_new_strava_token_data(refresh_token: str) -> dict | None:
    """
        Fetches new token from Strava API

        :param refresh_token: token for refreshing Strava token
        :returns:
            dict | None: Returns new Strava token_data if successful
    """
    logger.info("Requesting new token data")
    try:
        response_data = post(
            STRAVA_TOKEN_API_ENDPOINT,
            data={
                "client_id": settings.STRAVA_CLIENT_ID,
                "client_secret": settings.STRAVA_CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            },
            timeout=settings.REQUEST_TIMEOUT
        )
        strava_token_data = response_data.json()
        return strava_token_data

    except HTTPError as _e:
        logger.error("Failed to fetch new token data")
        return None

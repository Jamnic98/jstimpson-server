from datetime import datetime
from typing import Annotated, Optional
from pymongo import ReturnDocument
from pydantic import BaseModel, BeforeValidator, Field, ValidationError

from app.factories.logger import logger
from app.factories.database import strava_tokens_collection
from app.utils.strava_token_utils import fetch_new_strava_token_data
from app.utils import DEFAULT_STRAVA_TOKEN_ID

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class StravaTokenModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=DEFAULT_STRAVA_TOKEN_ID)
    access_token: str
    refresh_token: str
    expires_at: int
    expires_in: int

    def is_token_valid(self) -> bool:
        # returns true if expiration timestamp is in the future
        return self.expires_at > datetime.timestamp(datetime.now())

    async def refresh(self) -> None:
        logger.info("Attempting to refresh Strava token")
        try:
            new_token_data = await fetch_new_strava_token_data(self.refresh_token)
            if not new_token_data:
                raise ValueError("Unable to refresh Strava token without new token data")
            # update database token
            new_strava_token = StravaTokenModel.model_validate(new_token_data)
            updated_token = await strava_tokens_collection.find_one_and_replace(
                {"_id": self.id},
                new_strava_token.model_dump(exclude={"id"}),
                return_document=ReturnDocument.AFTER,
                upsert=True
            )
            # update local token
            self.access_token, self.refresh_token, self.expires_at, self.expires_in = (
                updated_token["access_token"],
                updated_token["refresh_token"],
                updated_token["expires_at"],
                updated_token["expires_in"]
            )
            logger.info("Successfully refreshed Strava token")

        except (ValueError, ValidationError) as e:
            logger.error("Failed to refresh Strava token: %s", e)

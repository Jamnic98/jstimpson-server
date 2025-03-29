from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

from app.utils.enums import SportType


# Represents an ObjectId field in the database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class ActivityModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, exclude=False)
    # athlete: dict | None
    name: str | None
    distance: float
    moving_time: int
    elapsed_time: int | None
    total_elevation_gain: float | None
    sport_type: SportType | None
    # workout_type: int | None
    strava_id: str | None
    # external_id: str | None
    upload_id: str | None
    start_date: datetime | None
    start_date_local: datetime
    timezone: str | None
    utc_offset: int | None
    # start_latlng: str | None
    # end_latlng: str | None
    location_city: str | None
    location_state: str | None
    location_country: str | None
    achievement_count: int | None
    # kudos_count: int | None
    # comment_count: int | None
    # athlete_count: int | None
    # photo_count: int | None
    # map: dict | None = Field(...
    # trainer: bool | None
    # commute: bool | None
    # manual: bool | None
    private: bool | None
    flagged: bool | None
    gear_id: str | None
    from_accepted_tag: bool | None
    average_speed: float | None
    max_speed: float | None
    average_cadence: float | None
    average_watts: float | None
    weighted_average_watts: float | None
    kilojoules: float | None
    device_watts: bool | None
    has_heartrate: bool | None
    average_heartrate: float | None
    max_heartrate: float | None
    max_watts: float | None
    pr_count: int | None
    # total_photo_count: int | None
    # has_kudoed: bool | None
    suffer_score: int | None


class ActivityCollection(BaseModel):
    activities: list[ActivityModel]

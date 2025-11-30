from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

from app.utils.enums import SportType


# Represents an ObjectId field in the database.
PyObjectId = Annotated[str, BeforeValidator(str)]


class ActivityModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    strava_id: Optional[str] = Field(None, alias="id")  # official Strava id
    name: Optional[str]
    distance: Optional[float]  # in meters
    moving_time: Optional[int]  # seconds
    elapsed_time: Optional[int]  # seconds
    total_elevation_gain: Optional[float]  # meters
    sport_type: Optional[SportType]
    start_date: Optional[datetime]
    start_date_local: Optional[datetime]
    timezone: Optional[str]
    upload_id: Optional[str]

    # Optional performance metrics
    average_speed: Optional[float]  # m/s
    max_speed: Optional[float]  # m/s
    average_watts: Optional[float]  # watts
    max_watts: Optional[int]
    weighted_average_watts: Optional[int]
    kilojoules: Optional[float]
    device_watts: Optional[bool]

    # Optional physiological data
    average_heartrate: Optional[float]
    max_heartrate: Optional[float]

    # Optional misc
    pr_count: Optional[int]
    suffer_score: Optional[int]


class ActivityCollection(BaseModel):
    activities: list[ActivityModel]

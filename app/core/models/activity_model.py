from enum import Enum
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class SportType(Enum):
    ALPINE_SKI = "AlpineSki"
    BACKCOUNTRY_SKI = "BackcountrySki"
    BADMINTON = "Badminton"
    CANOEING = "Canoeing"
    CROSSFIT = "Crossfit"
    E_BIKE_RIDE = "EBikeRide"
    ELLIPTICAL = "Elliptical"
    E_MOUNTAIN_BIKE_RIDE = "EMountainBikeRide"
    GOLF = "Golf"
    GRAVEL_RIDE = "GravelRide"
    HANDCYCLE = "Handcycle"
    HIGH_INTENSITY_INTERVAL_TRAINING = "HighIntensityIntervalTraining"
    HIKE = "Hike"
    ICE_SKATE = "IceSkate"
    INLINE_SKATE = "InlineSkate"
    KAYAKING = "Kayaking"
    KITESURF = "Kitesurf"
    MOUNTAIN_BIKE_RIDE = "MountainBikeRide"
    NORDIC_SKI = "NordicSki"
    PICKLEBALL = "Pickleball"
    PILATES = "Pilates"
    RACQUETBALL = "Racquetball"
    RIDE = "Ride"
    ROCK_CLIMBING = "RockClimbing"
    ROLLER_SKI = "RollerSki"
    ROWING = "Rowing"
    RUN = "Run"
    SAIL = "Sail"
    SKATEBOARD = "Skateboard"
    SNOWBOARD = "Snowboard"
    SNOWSHOE = "Snowshoe"
    SOCCER = "Soccer"
    SQUASH = "Squash"
    STAIR_STEPPER = "StairStepper"
    STAND_UP_PADDLING = "StandUpPaddling"
    SURFING = "Surfing"
    SWIM = "Swim"
    TABLE_TENNIS = "TableTennis"
    TENNIS = "Tennis"
    TRAIL_RUN = "TrailRun"
    VELOMOBILE = "Velomobile"
    VIRTUAL_RIDE = "VirtualRide"
    VIRTUAL_ROW = "VirtualRow"
    VIRTUAL_RUN = "VirtualRun"
    WALK = "Walk"
    WEIGHT_TRAINING = "WeightTraining"
    WHEELCHAIR = "Wheelchair"
    WINDSURF = "Windsurf"
    WORKOUT = "Workout"
    YOGA = "Yoga"


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

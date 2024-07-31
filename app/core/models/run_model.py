from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class RunModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, exclude=True)
    distance: float
    duration: int
    start_date_local: datetime


class RunCollection(BaseModel):
    runs: list[RunModel]

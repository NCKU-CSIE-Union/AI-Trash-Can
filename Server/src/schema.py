from typing import Optional, Annotated
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator, field_validator

PyObjectId = Annotated[str, BeforeValidator(str)]


# Define the Record model
class Record(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    seen: bool | None = None
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True,
    )


class HeatMapRecord(BaseModel):
    date: Optional[PyObjectId] = Field(alias="_id", default=None)
    value: int


class Filters(BaseModel):
    seen: bool | None = None
    created_at_start: datetime | None = None
    created_at_end: datetime | None = None


class SystemEvent(BaseModel):
    event_type: str = "system"
    message: str


class NewRecordEvent(BaseModel):
    event_type: str = "new_record"
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

from typing import Optional, Annotated
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator

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

class Filters(BaseModel):
    seen: bool = None
    created_at_start: datetime = None
    created_at_end: datetime = None
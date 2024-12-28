from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class BaseEntityModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        extra="ignore",  # maybe set as forbid for better validation
    )
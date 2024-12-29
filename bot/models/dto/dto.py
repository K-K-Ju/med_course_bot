from typing import Annotated

from pydantic import Field

from bot.models.base import BaseEntityModel


class DTO(BaseEntityModel):
    idx: Annotated[int, Field(alias="id", gt=0)]

from typing import Annotated

from pydantic import Field

from bot.models.dto.dto import DTO
from bot.static.enums.states import State


class AdminDTO(DTO):
    state: Annotated[State, Field()]

from typing import Annotated

from pydantic import Field

from bot.models.dto.dto import DTO
from bot.static.enums.states import State


class ClientDTO(DTO):
    idx: Annotated [str, Field()]
    username: Annotated[str, Field()]
    name: Annotated[str, Field()]
    phone_number: Annotated[str, Field()]
    state: Annotated[State, Field()]

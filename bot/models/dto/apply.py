from typing import Annotated

from pydantic import Field

from bot.models.dto.dto import DTO
from bot.static.enums.states import ApplyState


class ApplyDTO(DTO):
    user_id: Annotated[str, Field()]
    lesson_id: Annotated[str, Field()]
    state: Annotated[ApplyState, Field()]

from typing import Annotated

from pydantic import Field

from bot.models.dto.dto import DTO
from bot.static.enums.states import ApplyState


class ApplyDTO(DTO):
    idx: Annotated[str, Field(default='0',)]
    user_id: Annotated[str, Field()]
    lesson_id: Annotated[str, Field()]
    state: Annotated[ApplyState, Field()]

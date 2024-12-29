from datetime import datetime
from typing import Annotated

from pydantic import Field

from bot.models.dto.dto import DTO


class LessonDTO(DTO):
    title: Annotated[str, Field()]
    datetime: Annotated[datetime, Field()]
    description: Annotated[str, Field()]

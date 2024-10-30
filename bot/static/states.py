from enum import Enum


class State(Enum):
    NOT_REGISTERED = 0
    BASE = 10
    PENDING_MANAGER = 11
    ACTIVE_ADMIN = 21


class ApplyState(Enum):
    NEW = 0
    BOOKED = 1
    CONFIRMED = 2
    DECLINED = 3


APPLY_STATE_TEXT_MAPPING: dict = {0: 'Новий', 1: 'Заброньвано', 2: 'Підтверджено', 3: 'Відхилено'}
from enum import Enum


class State(Enum):
    NOT_REGISTERED = 0
    REGISTERED = 10
    PENDING_MANAGER = 11

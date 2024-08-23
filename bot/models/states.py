from enum import Enum


class States(Enum):
    FREE = 0
    BOOK_PENDING_MSG = 1
    BOOK_APPROVED = 2
    PENDING_MSG = 3
    APPROVED = 4


